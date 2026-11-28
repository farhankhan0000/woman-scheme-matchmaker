import json
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from backend.models import Schemes
from backend.ai import get_embedding



load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing from the root .env file")



sync_engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)



SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False
)



SCHEMES_FILE = Path(__file__).resolve().parent / "schemes.json"


def seed_database():


    with SCHEMES_FILE.open("r", encoding="utf-8") as file:
        schemes_data = json.load(file)


    if isinstance(schemes_data, dict):
        schemes_data = [schemes_data]

    if not isinstance(schemes_data, list):
        raise ValueError("Expected a JSON object or list of objects")

    if not all(isinstance(item, dict) for item in schemes_data):
        raise ValueError("Every scheme must be a JSON object")


    with SyncSessionLocal() as session:
        result = session.execute(
            select(Schemes.scheme_code)
        )

        existing_codes = set(result.scalars().all())


    new_schemes = []
    skipped_count = 0

    for data in schemes_data:

        scheme_code = data["scheme_code"]

        if scheme_code in existing_codes:
            print(f"Skipping {scheme_code} - Already exists")
            skipped_count += 1
            continue

        existing_codes.add(scheme_code)


        embedding = get_embedding(data["embedding_text"])

        if embedding is None or len(embedding) != 768:
            raise ValueError(
                f"Invalid embedding dimensions for {scheme_code}"
            )


        new_scheme = Schemes(
            scheme_code=data["scheme_code"],
            title_en=data["title_en"],
            summary_en=data["summary_en"],
            target_gender=data["target_gender"],
            has_women_carve_out=data["has_women_carve_out"],
            eligible_states=data["eligible_states"],
            min_age=data["min_age"],
            max_age=data["max_age"],
            min_loan_amount=data["min_loan_amount"],
            max_loan_amount=data["max_loan_amount"],
            max_turnover_limit=data["max_turnover_limit"],
            allowed_sectors=data["allowed_sectors"],
            subsidy_percentage=data["subsidy_percentage"],
            min_promoter_margin_percentage=data["min_promoter_margin_percentage"],
            interest_rate_percentage=data["interest_rate_percentage"],
            requires_udyam=data["requires_udyam"],
            requires_gst=data["requires_gst"],
            other_registrations=data["other_registrations"],
            embedding_text=data["embedding_text"],
            scheme_specific_fields=data["scheme_specific_fields"],
            embedding=embedding
        )

        new_schemes.append(new_scheme)


    if new_schemes:

        with SyncSessionLocal() as session:

            try:
                session.add_all(new_schemes)

                session.commit()

            except Exception:
                session.rollback()
                raise


    print(
        f"Seeding completed: "
        f"{len(new_schemes)} inserted, "
        f"{skipped_count} skipped."
    )


def main():

    try:
        seed_database()

    finally:
        sync_engine.dispose()


if __name__ == "__main__":
    main()