import enum

class GenderType(enum.Enum):
    MALE = "male"
    FEMALE = "female"

class Role(enum.Enum):
    OWNER = "owner"
    MANAGER = "manager"
    EMPLOYEE = "employee"
