from datetime import datetime
from functools import lru_cache
from math import log
from typing import Optional
from uuid import UUID

from src.core.client import CustomAsyncClient, get_custom_client
from src.schemas.scoring import ScoreIn


class LogarithmError(Exception):
    pass


class ScoreNotFoundError(Exception):
    pass


class ScoreService:
    def __init__(self, client: CustomAsyncClient) -> None:
        self.client = client

    async def _get_scores(
        self,
        accommodation_id: UUID,
        time_frame: str,
        offset: int,
        limit: int,
        url: str = "http://localhost:8000",
    ) -> dict:
        full_url = f"{url}/accommodations/{accommodation_id}/reviews"
        reviews = await self.client.get(
            full_url,
            params={"offset": offset, "limit": limit, "status": "approved", "time_frame": time_frame},
        )
        return reviews

    async def get_new_scores(
        self,
        accommodation_id: UUID,
        offset: int,
        limit: int,
        score_aspect: Optional[str] = None,
    ) -> list[ScoreIn]:
        new_scores = await self._get_scores(accommodation_id, "newer_than_2_years", offset, limit)
        if score_aspect is None:
            return [ScoreIn(**new_score) for new_score in new_scores]
        return [ScoreIn(**new_score) for new_score in new_scores if score_aspect in new_score["score_aspects"]]

    async def compute_new_score(
        self,
        accommodation_id: UUID,
        score_aspect: Optional[str] = None,
    ) -> dict[UUID, tuple]:
        """
        return: dict[uuid: (score, weight).
        raise: LogarithmError.
        """
        (
            start,
            end,
        ) = (
            0,
            1000,
        )
        new_scores = await self.get_new_scores(accommodation_id, start, end)
        new_scores_mapper = {}
        while new_scores:
            for new_score in new_scores:
                updated_at_month = new_score.updated_at.month
                current_month = datetime.utcnow().month
                arg = 25 - (current_month - updated_at_month)
                if arg <= 0:
                    raise LogarithmError(f"Argument={arg} was less than 0")

                score = new_score.general_score if score_aspect is None else new_score.score_aspects[score_aspect]
                weigth = log(arg)
                new_scores_mapper[new_score.id] = (weigth * score, weigth)
            start = end + 1
            end = end + 1000
            new_scores = await self.get_new_scores(accommodation_id, start, end)

        return new_scores_mapper

    async def get_old_scores(
        self,
        accommodation_id: UUID,
        offset: int,
        limit: int,
        score_aspect: Optional[str] = None,
    ) -> list[int]:
        old_scores = await self._get_scores(accommodation_id, "older_than_2_years", offset, limit)
        if score_aspect is None:
            return [ScoreIn(**old_score).general_score for old_score in old_scores]

        return [
            ScoreIn(**old_score).score_aspects[score_aspect]
            for old_score in old_scores
            if score_aspect in old_score["score_aspects"]
        ]

    async def compute_old_score(
        self,
        accommodation_id: UUID,
        coefficient: float = 1.77,
        score_aspect: Optional[str] = None,
    ) -> tuple[float, float]:
        """
        return: score, weight.
        raise: ScoreNotFoundError.
        """
        start, end, score_sum, amount = 0, 1000, 0, 0
        old_scores = await self.get_old_scores(accommodation_id, start, end, score_aspect)
        while old_scores:
            score_sum += sum(old_scores)
            amount += len(old_scores)
            start = end + 1
            end = end + 1000
            old_scores = await self.get_old_scores(accommodation_id, start, end, score_aspect)

        if amount == 0:
            raise ScoreNotFoundError("Score was not found")

        weight = log(coefficient)
        return (score_sum / amount) * weight, weight

    async def compute_overall_score(
        self,
        accommodation_id: UUID,
        score_aspect: Optional[str] = None,
    ) -> dict:
        weighted_old_score, weight = await self.compute_old_score(accommodation_id, score_aspect=score_aspect)
        weighted_new_scores = await self.compute_new_score(accommodation_id, score_aspect=score_aspect)
        numerator = weighted_old_score
        denominator = weight
        for weighted_new_score, weight in weighted_new_scores.values():
            numerator += weighted_new_score
            denominator += weight
        result = numerator / denominator
        if score_aspect is None:
            return {"general_score": round(result, 2)}

        return {score_aspect: round(result, 2)}

    async def get_general_score(
        self,
        accommodation_id: UUID,
    ) -> dict:
        return await self.compute_overall_score(accommodation_id)

    async def get_score_aspect(
        self,
        accommodation_id: UUID,
        score_aspect: str,
    ) -> dict:
        return await self.compute_overall_score(accommodation_id, score_aspect=score_aspect)


@lru_cache
def get_score_service() -> ScoreService:
    return ScoreService(get_custom_client())
