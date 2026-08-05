from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, StringConstraints
from app.schemas.preference_schema import CustomerPreferencesSchema

class CustomerRegistrationSchema(BaseModel):
    first_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
    last_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
    middle_name: Optional[str] = Field(default=None, max_length=100)
    preferred_name: Optional[str] = Field(default=None, max_length=100)
    email: EmailStr = Field(..., max_length=255)
    plan_name: str = Field(default= "Standard Smoothie Plan", max_length=100)
    start_date: Optional[str] = Field(default=None)
    end_date: Optional[str] = Field(default=None)
    preferences: CustomerPreferencesSchema = Field(default_factory=CustomerPreferencesSchema)
        
class RegistrationResponseData(BaseModel):
    customer_id: str
    subscription_id: str
    subscription_status: str
    preference_id: str
    
class ApiResponse(BaseModel):
    status: str
    message: str
    data: Optional[RegistrationResponseData] = None
    errors: Optional[dict] = None    