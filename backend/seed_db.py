import json
from sqlalchemy.orm import Session
from database import engine,Base
from models import Schemes

Base.metadata.create_all(bind=engine)

def seed_database():
    with Session(engine) as session:
        with open("schemes.json", "r", encoding="utf-8") as file:
            schemes_data=json.load(file)

        if isinstance(schemes_data, dict):
            schemes_data = [schemes_data]

        for data in schemes_data:
            exists = session.query(Schemes).filter(Schemes.scheme_code == data["scheme_code"]).first()
            if exists:
                print(f"Skipping {data['scheme_code']} - Already exists in the table")
                continue
            placeholder_vector = [0.0] * 768

            new_scheme = Schemes(
                schemes_code = data["scheme_code"],
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
                embedding=placeholder_vector
            )
            session.add(new_scheme)

        session.commit()
        print("Database successfully seeded with scheme data!")

if __name__ == "__main__":
    seed_database()
