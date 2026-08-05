
from pydantic import BaseModel, Field


class CustomerPreferencesSchema(BaseModel):
    profile_name: str = Field(default="Default Profile", max_length=100)
    days: int = Field(default=7, ge=1, le=30)
    max_calories: int = Field(default=500, ge=100, le=3000)
    nut_free: bool = Field(default=False)
    gluten_free: bool = Field(default=False)
    dairy_free: bool = Field(default=False)
    soy_free: bool = Field(default=False)