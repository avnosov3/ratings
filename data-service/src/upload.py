import argparse
import asyncio
import logging

from src.core.config import settings
from src.repositories.accommodation import get_accommodation_repository, get_amenity_repository, get_file_repository
from src.repositories.review import get_locale_repository, get_review_repository, get_source_repository
from src.repositories.user import get_user_repository
from src.services.import_data import ImportDataService


async def import_data(accommodations_path: str, reviews_path: str):
    import_data_service = ImportDataService(
        f"{settings.BASE_DIR}/{accommodations_path}",
        f"{settings.BASE_DIR}/{reviews_path}",
        get_accommodation_repository(),
        get_file_repository(),
        get_amenity_repository(),
        get_review_repository(),
        get_locale_repository(),
        get_source_repository(),
        get_user_repository(),
    )
    result = await import_data_service.run()
    logging.info(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("accommodations_path", type=str, help="Path to accommodations file")
    parser.add_argument("reviews_path", type=str, help="Path to reviews file")
    args = parser.parse_args()
    asyncio.run(import_data(args.accommodations_path, args.reviews_path))


if __name__ == "__main__":
    main()
