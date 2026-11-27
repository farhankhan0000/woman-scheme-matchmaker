
from backend.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

class Schemes(Base):
    __tablename__="scheme_table"
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    scheme_code = Column(String, nullable=False)
    title_en = Column(String, nullable=False)
    summary_en = Column(String, nullable=False)
    target_gender = Column(String, nullable=False)
    has_women_carve_out = Column(Boolean, nullable=False)
    eligible_states = Column(ARRAY(String), nullable=False, default=list)
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
    scheme_specific_fields = Column(JSONB, nullable=False)
    embedding = Column(Vector(768))

class AgentState(Base):
    __tablename__="agent_state"
    id=Column(Integer, primary_key=True,nullable=False,unique=True)
    conversation_id=Column(Integer,ForeignKey("conversation.id", ondelete="CASCADE"),unique=True,nullable=False)
    business_idea=Column(String, nullable=True)
    business_stage=Column(String, nullable=True)
    state=Column(String, nullable=True)
    social_category=Column(String, nullable=True)
    funding_needed=Column(Integer, nullable=True)
    gender=Column(String, default="female", nullable=False)

class User(Base):
    __tablename__="user_login_info"
    id=Column(Integer, primary_key=True,nullable=False,unique=True)
    name=Column(String, nullable=False)
    user_name=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)

class Conversation(Base):
    __tablename__="conversation"
    id=Column(Integer, primary_key=True,nullable=False,unique=True)
    user_id=Column(Integer, ForeignKey("user_login_info.id", ondelete="CASCADE"), nullable=False, index=True)
    title=Column(String,default="New Chat", nullable=False)

class Messages(Base):
    __tablename__="messages"
    id=Column(Integer, primary_key=True, nullable=False, unique=True)
    conversation_id=Column(Integer, ForeignKey("conversation.id", ondelete="CASCADE"), nullable=False, index=True)
    role=Column(String, nullable=False)
    content=Column(Text,nullable=False)



