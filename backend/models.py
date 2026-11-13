from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

class Schemes(Base):
    __tablename__="scheme_table"
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    scheme_code = Column(String, nullable=False)
    title_en = Column(String, nullable=False)
    title_hi = Column(String, nullable=False)
    summary_en = Column(String, nullable=False)
    summary_hi = Column(String, nullable=False)
    target_gender = Column(String, nullable=False)
    has_women_carve_out = Column(Boolean, nullable=False)
    eligible_status = Column(ARRAY(String), nullable=False, default=list)
    min_age = Column(Integer, nullable=False)
    max_age = Column(Integer, nullable=False)
    min_loan_amount = Column(Integer, nullable=False)
    max_loan_amount = Column(Integer, nullable=False)
    max_turnover_limit = Column(Integer, nullable=True)
    allowed_sectors = Column(ARRAY(String), nullable=False)
    subsidy_percentage = Column(Float, nullable=False)
    min_promoter_margin_percentage = Column(Float, nullable=False)
    interest_rate_percentage = Column(Float, nullable=False)
    requires_udyam = Column(Boolean, nullable=False)
    requires_gst = Column(Boolean, nullable=False)
    other_registrations = Column(ARRAY(String), nullable=True)
    embedding_text = Column(String, nullable=False)
    form_schema = Column(JSONB, nullable=False)
    embedding = Column(Vector(768))