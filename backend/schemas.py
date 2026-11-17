from pydantic import BaseModel, Field
from typing import Optional, Literal


IndianStateOrUT = Literal["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"]

MasterBusinessSector = Literal["Food Processing", "Manufacturing", "Textiles", "Handicrafts",
    "Services", "Retail", "Agriculture", "Education & Healthcare",
    "Transport & Logistics", "IT & Technology"]

class SchemeSpecificFields(BaseModel):
    name: str
    label_en: str
    type: str
    options: list[str]
    required: bool

class UserInfo(BaseModel):
    applicant_name: str=Field(description="Full legal name as per Aadhaar")
    age: int=Field(description="Used for database SQL filtering")
    gender: Literal["Female", "Male", "Other"] = Field(description="Target Gender")
    social_category:  Literal["General", "SC", "ST", "OBC", "MINORITY"]

    aadhaar_number: str=Field(description="Required for final DPR generation")
    pan_number: str=Field(description="Required for commercial loan KYC")

    state_or_ut: IndianStateOrUT = Field(description="Applicant's State or Union Territory")
    residential_address: str=Field(description="Applicant's Home address")
    residential_pincode: int=Field(description="Applicant's Home pin code")
    is_business_address_same: bool = Field(
        default=True,
        description="True if operating from home, False if separate location"
    )
    district: str=Field(description="Required for the DPR")
    business_address: str=Field(description="Physical location of the enterprise")
    business_pincode: int=Field(description="pin code of the location of the enterprise")

    business_sector: MasterBusinessSector = Field(..., description="Used for SQL filtering (allowed_sectors)")
    is_new_business: bool = Field(..., description="True if setting up, False if upgrading")
    project_cost: int = Field(..., description="Used to calculate subsidy % and promoter margin")

    bank_name: str = Field(..., description="Name of the applicant's bank")
    account_number: str = Field(..., description="Applicant's bank account number")
    ifsc_code: str = Field(..., description="Branch specific IFSC code")
