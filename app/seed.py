from app.database import SessionLocal
from app.models.employee import Employee, SkillLevel
from app.models.customer import Customer
from app.models.service import Service, ServiceCategory
from app.models.enums import GenderType

def seed():
    db = SessionLocal()

    employees = [
        Employee(name="Anna Nguyen", phone="9185550101", gender=GenderType.FEMALE, skill_level=SkillLevel.BOTH, is_employed=True, is_active=False),
        Employee(name="Jenny Tran", phone="9185550102", gender=GenderType.FEMALE, skill_level=SkillLevel.HAND, is_employed=True, is_active=False),
        Employee(name="Kevin Le", phone="9185550103", gender=GenderType.MALE, skill_level=SkillLevel.BOTH, is_employed=True, is_active=False),
        Employee(name="Lisa Pham", phone="9185550104", gender=GenderType.FEMALE, skill_level=SkillLevel.FOOT, is_employed=True, is_active=False),
    ]

    customers = [
        Customer(name="Sarah Smith", phone="9181234001", gender=GenderType.FEMALE, birthday="1990-05-15"),
        Customer(name="Emily Johnson", phone="9181234002", gender=GenderType.FEMALE, birthday="1985-08-22"),
        Customer(name="Michael Brown", phone="9181234003", gender=GenderType.MALE),
        Customer(name="Jessica Davis", phone="9181234004", gender=GenderType.FEMALE, birthday="1995-03-10"),
    ]

    services = [
        Service(name="Manicure Basic", category=ServiceCategory.HAND, base_price=25),
        Service(name="Manicure Gel", category=ServiceCategory.HAND, base_price=38),
        Service(name="Fullset Acrylic", category=ServiceCategory.HAND, base_price=55),
        Service(name="Fullset Dip", category=ServiceCategory.HAND, base_price=50),
        Service(name="Pedicure Basic", category=ServiceCategory.FOOT, base_price=30),
        Service(name="Pedicure Deluxe", category=ServiceCategory.FOOT, base_price=49),
        Service(name="Pedicure Luxury", category=ServiceCategory.FOOT, base_price=63),
        Service(name="Parafin Wax", category=ServiceCategory.ADDON, base_price=10),
        Service(name="Neck Massage", category=ServiceCategory.ADDON, base_price=10),
    ]

    db.add_all(employees)
    db.add_all(customers)
    db.add_all(services)
    db.commit()
    db.close()
    print("Seed data added succesfully")

if __name__ == "__main__":
    seed()