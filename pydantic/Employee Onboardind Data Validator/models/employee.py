from .address import Address
from .bank_details import BankDetails
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, computed_field
from typing import Annotated, List, Optional
from datetime import date

class Employee(BaseModel):
    employee_id: Annotated[str, Field(pattern=r'EMP\d{4}$')]
    full_name: str
    email: EmailStr
    phone: str
    age: Annotated[int, Field(ge=18, le=65)]
    department: str
    joining_date: date
    salary: Annotated[float, Field(ge=0, strict=True)]
    address: Address
    bank_details: BankDetails
    skills: Annotated[List[str], Field(default=[], max_length=10)]
    emergency_contact: Optional[str] = None

    @field_validator('full_name')
    @classmethod
    def normalize_name(cls, name):
        return name.strip().title()
    
    @field_validator('phone')
    @classmethod
    def validate_phone_number(cls, value):
        digits = value.replace('+1', '').replace(' ', '').replace('-', '')
        if not digits.isdigit() or len(digits) != 10:
            raise ValueError(f'Invalid phone number: {value}')
        return digits

    @model_validator(mode='after')
    def check_emergency_contact(cls, model):
        if model.age > 50 and not model.emergency_contact:
            raise ValueError('Employees above 50 years must have an emergency contact')
        return model
    
    @computed_field
    @property
    def retires_in_years(self) -> Annotated[int, Field(ge=0)]:
        return max(0, 65 - self.age)

    @computed_field
    @property
    def no_of_years_joined(self) -> Annotated[int, Field(ge=0)]:
        return (date.today() - self.joining_date).days // 365