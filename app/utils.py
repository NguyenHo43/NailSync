from fastapi import HTTPException

def get_or_404(db, model, id, detail="Not found"):
    obj = db.query(model).filter(model.id==id).first()
    if not obj:
        raise HTTPException(status_code=404, detail=detail)
    
    return obj