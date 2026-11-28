import json
from sqlalchemy.orm import Session
from database import engine,SessionLocal
from models import Schemes
from ai import get_embedding
import asyncio
from sqlalchemy import select


async def seed_database():
    with Session(engine) as session:
        with open("schemes.json", "r", encoding="utf-8") as file:
            schemes_data=json.load(file)

        if isinstance(schemes_data, dict):
            schemes_data = [schemes_data]

        async with SessionLocal() as session:
            try:

                for data in schemes_data:
                    result = await session.execute(select(Schemes.id).where(Schemes.scheme_code==data["scheme_code"]).limit(1))
                    exists = result.scalar_one_or_none()
                    if exists is not None:
                        print(f"Skipping {data['scheme_code']} - Already exists in the table")
                        continue
                    embedding = await asyncio.to_thread(
                        get_embedding,
                        data["embedding_text"]
                    )

                    new_scheme = Schemes(
                        scheme_code = data["scheme_code"],
                        title_en = data["title_en"],
                        summary_en = data["summary_en"],
                        target_gender = data["target_gender"],
                        has_women_carve_out = data["has_women_carve_out"],
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
                    session.add(new_scheme)

                await session.commit()
                print("Database successfully seeded with scheme data!")

            except Exception:
                await session.rollback()
                raise

if __name__ == "__main__":
    seed_database()
