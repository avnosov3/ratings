from math import log
from unittest.mock import AsyncMock

import pytest

from src.services.scoring import ScoreNotFoundError, ScoreService


class TestScoring:
    async def test_compute_overall_score_if_score_not_found(self, score_service: ScoreService):
        score_service.compute_overall_score = AsyncMock(side_effect=ScoreNotFoundError("Score was not found"))
        with pytest.raises(ScoreNotFoundError, match="Score was not found"):
            await score_service.get_general_score("123e4567-e89b-12d3-a456-426614174000")

    async def test_compute_overall_score_success(self, score_service: ScoreService):
        score_service.compute_old_score = AsyncMock(return_value=(10.0, 2.0))
        score_service.compute_new_score = AsyncMock(return_value={"aspect1": (30.0, 3.0)})

        result = await score_service.compute_overall_score("123e4567-e89b-12d3-a456-426614174000")

        assert result == {"general_score": 8.0}, "The computed overall score should be correct."

    async def test_compute_old_score_no_scores(self, score_service: ScoreService):
        score_service.get_old_scores = AsyncMock(return_value=[])

        with pytest.raises(ScoreNotFoundError, match="Score was not found"):
            await score_service.compute_old_score("123e4567-e89b-12d3-a456-426614174000")

    async def test_compute_old_score_success(self, score_service: ScoreService):
        score_service.get_old_scores = AsyncMock(
            side_effect=[
                [10, 15, 10, 15],
                [20, 25],
                [],
            ],
        )

        score, weight = await score_service.compute_old_score("123e4567-e89b-12d3-a456-426614174000")

        assert round(score, 2) == 9.04
        assert weight == log(1.77)
