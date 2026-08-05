

from typing import List
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    location: List[str | int] = Field(..., description="Location of the error in the request data")
    message: str = Field(..., description="Error message describing the error")
    type: str = Field(..., description="Type of the error")
    
class ErrorResponseSchema(BaseModel):
    message: str = Field(..., description="General error message")
    errors: List[ErrorDetail] = Field(..., description="List of detailed error information")