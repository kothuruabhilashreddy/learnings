from pydantic import BaseModel, Field, field_validator
from typing import Annotated

class Address(BaseModel):
    street: str
    city: str
    state: str
    pincode: str

    @field_validator('pincode')
    @classmethod
    def validate_pincode(cls, value):
        if not value.isdigit() or len(value) != 5:
            raise ValueError('Pincode must be 5-digit number')
        return value
