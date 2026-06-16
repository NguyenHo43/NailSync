from fastapi import HTTPException
from app.models.employee import Employee, SkillLevel
def get_or_404(db, model, id, detail="Not found"):
    obj = db.query(model).filter(model.id==id).first()
    if not obj:
        raise HTTPException(status_code=404, detail=detail)
    
    return obj

def check_duplicate(db, model, field, value, detail="Already exists"):
    existing = db.query(model).filter(field==value).first()
    if existing:
        raise HTTPException(status_code=400, detail=detail)
    
def find_available_employee(db, skill):
    return db.query(Employee).filter(
        Employee.is_employed==True,
        Employee.is_active==True,
        Employee.is_busy==False,
        Employee.skill_level.in_([skill, SkillLevel.BOTH])).order_by(Employee.turn_order).first()