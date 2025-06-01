from app.models.user import User
from app.models.record import Record
from sqlalchemy.orm import Session
from fastapi import HTTPException


async def get_records(current_user: User, db: Session):
    """
    Get all records for the current user.
    """

    records = db.query(Record).filter(Record.student_id == current_user.id).order_by(Record.created_at).all()
    
    if not records:
        raise HTTPException(status_code=404, detail="No records found")

    return {
        "message": "Records retrieved successfully",
        "records": [record.to_dict() for record in records]
    }


async def add_record(current_user: User, db: Session, class_id: int):
    """
    Add a new record for the current user.
    """
    
    try:
        new_record = Record(
            student_id=current_user.id,
            student_name=current_user.student_name,
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        
        return {
            "message": "Record added successfully",
            "record": new_record.to_dict()
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add record: {str(e)}")
    

async def delete_record(current_user: User, db: Session, record_id: int):
    """
    Delete a record by ID for the current user.
    """
    
    record = db.query(Record).filter(Record.id == record_id, Record.student_id == current_user.id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    db.delete(record)
    db.commit()
    
    return {
        "message": "Record deleted successfully",
        "record_id": record_id
    }