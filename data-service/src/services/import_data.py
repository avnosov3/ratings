import json
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.db import get_async_engine, get_async_session_maker
from src.models.accommodation import Accommodation, Amenity, File
from src.models.review import Review
from src.repositories.accommodation import AccommodationRepository, AmenityRepository, FileRepository
from src.repositories.review import LocaleRepository, ReviewRepository, SourceRepository
from src.repositories.user import UserRepository
from src.schemas.accommodation import AccommodationIn, AmenityIn, FileIn
from src.schemas.review import LocaleIn, ReviewIn, SourceIn
from src.schemas.user import UserIn


class ImportDataService:
    SUCCESS = "SUCCESS"

    def __init__(
        self,
        accommodation_file: str,
        reviews_file: str,
        accommodation_repository: AccommodationRepository,
        file_repository: FileRepository,
        amenity_repository: AmenityRepository,
        review_repository: ReviewRepository,
        locale_repository: LocaleRepository,
        source_repository: SourceRepository,
        user_repository: UserRepository,
    ):
        self.accommodation_file = accommodation_file
        self.reviews_file = reviews_file
        self.accommodation_repository = accommodation_repository
        self.file_repository = file_repository
        self.amenity_repository = amenity_repository
        self.review_repository = review_repository
        self.locale_repository = locale_repository
        self.source_repository = source_repository
        self.user_repository = user_repository
        self.objs_to_db = []
        self.accommodation_mapper = {}
        self.user_mapper = {}
        self.source_mapper = {}
        self.locale_mapper = {}
        self.amenity_mapper = {}

    async def _proccess_accommodation(
        self,
        accommodation: dict,
        session: AsyncSession,
        commit: bool = False,
    ) -> Accommodation:
        accommodation_in = AccommodationIn.build(accommodation)
        accommodation_db = await self.accommodation_repository.create(
            accommodation_in.model_dump(),
            session,
            commit=commit,
        )
        self.accommodation_mapper[str(accommodation_in.id)] = accommodation_db
        self.objs_to_db.append(accommodation_db)
        return accommodation_db

    async def _proccess_file(
        self,
        file: dict,
        accommodation_db: Accommodation,
        defult_media_id: UUID,
        session: AsyncSession,
        commit: bool = False,
    ) -> File:
        file_in = FileIn(
            **file,
            accommodation=accommodation_db,
            is_default=file["id"] == defult_media_id,
        )
        file_db = await self.file_repository.create(
            file_in.model_dump(),
            session,
            commit=commit,
        )
        self.objs_to_db.append(file_db)
        return file_db

    async def _proccess_amenity(
        self,
        amenity: str,
        accommodation_db: Accommodation,
        session: AsyncSession,
        commit: bool = False,
    ) -> Amenity:
        if amenity not in self.amenity_mapper:
            amenity_in = AmenityIn(name=amenity)
            amenity_db = await self.amenity_repository.create(
                amenity_in.model_dump(),
                session,
                commit=commit,
            )
            self.objs_to_db.append(amenity_db)
            self.amenity_mapper[amenity] = amenity_db
        accommodation_db.amenities.append(self.amenity_mapper[amenity])
        return self.amenity_mapper[amenity]

    async def _proccess_source(
        self,
        review: dict,
        session: AsyncSession,
        commit: bool = False,
    ):
        source_in = SourceIn(**review)
        if source_in.name not in self.source_mapper:
            source = await self.source_repository.create(
                source_in.model_dump(),
                session,
                commit=commit,
            )
            self.source_mapper[source_in.name] = source
            self.objs_to_db.append(source)

    async def _proccess_locale(
        self,
        review: dict,
        session: AsyncSession,
        commit: bool = False,
    ):
        locale_in = LocaleIn(**review)
        if locale_in.code not in self.locale_mapper:
            locale = await self.locale_repository.create(
                locale_in.model_dump(),
                session,
                commit=commit,
            )
            self.locale_mapper[locale.code] = locale
            self.objs_to_db.append(locale)

    async def _proccess_user(
        self,
        review: dict,
        session: AsyncSession,
        commit: bool = False,
    ):
        user_in = UserIn(**review)
        if user_in.email not in self.user_mapper:
            user = await self.user_repository.create(
                user_in.model_dump(),
                session,
                commit=commit,
            )
            self.user_mapper[user.email] = user
            self.objs_to_db.append(user)

    async def _proccess_review(
        self,
        review: dict,
        session: AsyncSession,
        commit: bool = False,
    ) -> Review:
        source_name = review.pop("source")
        locale_code = review.pop("locale")
        accommodation_id = review.pop("accommodationId")
        user_email = review.pop("userEmail")
        review_in = ReviewIn(
            **review,
            source=self.source_mapper[source_name],
            locale=self.locale_mapper[locale_code],
            user=self.user_mapper[user_email],
            accommodation=self.accommodation_mapper[accommodation_id],
            score_aspects=json.loads(review["scoreAspects"]),
        )
        review_db = await self.review_repository.create(
            review_in.model_dump(),
            session,
            commit=commit,
        )
        self.objs_to_db.append(review_db)
        return review_db

    async def run(self):
        engine = get_async_engine(settings.DATABASE_URL)
        async_session = get_async_session_maker(engine)
        async with async_session() as session:
            with open(self.accommodation_file, "r", encoding="utf-8") as file:
                accommodations = json.load(file)

            for accommodation in accommodations:
                accommodation_db = await self._proccess_accommodation(accommodation, session)
                defult_media_id = accommodation["defaultMedia"]["id"]

                for file in accommodation["topImages"]:
                    await self._proccess_file(
                        file,
                        accommodation_db,
                        defult_media_id,
                        session,
                    )

                for amenity in accommodation["filters"]:
                    await self._proccess_amenity(amenity, accommodation_db, session)

            with open(self.reviews_file, "r", encoding="utf-8") as file:
                reviews = json.load(file)

            for review in reviews:
                await self._proccess_source(review, session)
                await self._proccess_locale(review, session)
                await self._proccess_user(review, session)
                await self._proccess_review(review, session)

            session.add_all(self.objs_to_db)
            await session.commit()

        return self.SUCCESS
