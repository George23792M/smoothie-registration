from typing import Annotated, Optional
from datetime import date
from pydantic import BaseModel, EmailStr, Field, StringConstraints, BeforeValidator
from app.schemas.preference_schema import CustomerPreferencesSchema

# Sanitization function for string
def sanitize_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = str(value).strip()
    
    if not cleaned or cleaned.lower() == "string":
        return None
    return cleaned

#Clean mandatory string fields
CleanStr = Annotated[Optional[str], BeforeValidator(sanitize_string), StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]

#Clean optional string fields
OptionalCleanStr = Annotated[Optional[CleanStr], BeforeValidator(sanitize_string)]

class CustomerRegistrationSchema(BaseModel):
    first_name: CleanStr = Field(default=None)
    last_name: CleanStr = Field(default=None)
    middle_name: OptionalCleanStr = Field(default=None)
    preferred_name: OptionalCleanStr = Field(default=None)
    email: EmailStr = Field(..., max_length=255)
    plan_name: CleanStr = Field(default="Standard Smoothie Plan")
    start_date: Optional[date] = Field(default=None, description="The start date of the subscription")
    end_date: Optional[date] = Field(default=None, description="The end date of the subscription")
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