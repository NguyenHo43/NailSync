from pydantic import BaseModel, field_validator

class PhoneModel(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, v):
        return ''.join(filter(str.isdigit,v))