from pydantic import BaseModel, field_validator, Field
from typing import Annotated
import re

class BankDetails(BaseModel):
    account_number: Annotated[str, Field(max_length=16, min_length=9)]
    ifsc_code: str
    bank_name: str

    @field_validator('ifsc_code')
    @classmethod
    def validate_ifsc_code(cls, code):
        pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
        if not re.match(pattern, code.upper()):
            raise ValueError(f'Invalid IFSC code: {code}')
        return code
