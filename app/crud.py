from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date

def list_expenses(db: Session, limit: int = 100):
    return db.query(models.Expense).order_by(models.Expense.date.desc(), models.Expense.id.desc()).limit(limit).all()

def create_expense(db: Session, exp: schemas.ExpenseCreate):
    exp_date = exp.date or date.today()
    db_obj = models.Expense(
        title=exp.title,
        amount=exp.amount,
        category=exp.category,
        date=exp_date
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()

def delete_expense(db: Session, expense_id: int):
    obj = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
