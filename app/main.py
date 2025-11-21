import os
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, database, schemas

app = FastAPI(title="Simple Expense Tracker API")

# CORS - keep simple; set CORS_ORIGINS in Render to your frontend domain in prod
CORS = os.getenv("CORS_ORIGINS", "*")
if CORS == "*":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    origins = [o.strip() for o in CORS.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# create tables on startup
@app.on_event("startup")
def on_startup():
    database.init_db()


# dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/expenses", response_model=List[schemas.ExpenseOut])
def read_expenses(db: Session = Depends(get_db)):
    return crud.list_expenses(db)


@app.post("/expenses", response_model=schemas.ExpenseOut, status_code=201)
def add_expense(payload: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, payload)


@app.get("/expenses/{expense_id}", response_model=schemas.ExpenseOut)
def read_one(expense_id: int, db: Session = Depends(get_db)):
    item = crud.get_expense(db, expense_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item


@app.delete("/expenses/{expense_id}", status_code=204)
def remove_expense(expense_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_expense(db, expense_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return {}


@app.get("/")
def get_home():
    return {"name": "Tejas"}
