import schema
from database import SessionLocal, engine
import model
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse

##for data validation importing 2
from enum import Enum
from fastapi.encoders import jsonable_encoder

##for registration form entries
from fastapi import Depends, FastAPI, Request, Form
from starlette.responses import RedirectResponse

##for updating the propertys
from starlette.responses import JSONResponse

##to call js from html
from fastapi.middleware.cors import CORSMiddleware
import json


model.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000"
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency
def get_database_session():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/properties", response_class=HTMLResponse)
async def fetch_properties(request: Request, db: Session = Depends(get_database_session)):
    records = db.query(model.Property).all()
    return templates.TemplateResponse("index.html", {"request": request, "properties": records})

@app.get("/add_property_form", response_class=HTMLResponse)
async def add_property_form(request: Request, db: Session = Depends(get_database_session)):
    records = db.query(model.Property).all()
    return templates.TemplateResponse("add_property.html", {"request": request, "properties": records})

@app.post("/add_property/")
async def add_property(db: Session = Depends(get_database_session), name: schema.Property.name = Form(...), address: schema.Property.address = Form(...), type: schema.Property.type = Form(...), rent: schema.Property.rent = Form(...)):
    property = model.Property(name=name, address=address, type=type, rent=rent)
    db.add(property)
    db.commit()
    return {'property_status':'Property added successfully !!!'}

@app.get("/update_property_form", response_class=HTMLResponse)
async def update_property_form(request: Request, db: Session = Depends(get_database_session)):
    records = db.query(model.Property).all()
    return templates.TemplateResponse("update_property.html", {"request": request, "properties": records})

@app.patch("/update_property/")
async def update_property(request: Request, db: Session = Depends(get_database_session)):
      requestBody = await request.json()
      property = db.query(model.Property).get(requestBody['name'])
      property.address = requestBody['address']
      db.commit()
      # db.refresh(property)
      return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
