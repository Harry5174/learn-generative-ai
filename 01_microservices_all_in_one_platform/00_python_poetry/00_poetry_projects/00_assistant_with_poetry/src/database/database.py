# database.py
import statistics
from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends,status
from sqlmodel import SQLModel, create_engine, Session, Field , select
from sqlalchemy import URL
from datetime import datetime

class QueryLog(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_query: str
    assistant_response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Location(SQLModel, table=True):
    name: str = Field(index=True, primary_key=True)
    location: str

# Database setup
def create_db_and_tables(database_url: str):
    engine = create_engine(database_url)
    SQLModel.metadata.create_all(engine)

def read_all_persons(engine):
    with Session(engine) as session:
        loc_data = session.exec(select(Location)).all()
        return loc_data

async def create_person(engine, person_data: Location):
    """
    Creates a new person record in the database.

    Args:
        person_data (Location): name and location of person. 

    Returns:
        Location: The created person record that is the name and location of the person. 
    """
    with Session(engine) as session:
        session.add(person_data)
        session.commit()
        session.refresh(person_data)
        return person_data

def get_location_or_404(name: str, engine):
    with Session(engine) as session:
        loc_data = session.exec(select(Location).where(Location.name == name)).first()
        if not loc_data:
            raise HTTPException(status_code=statistics.HTTP_404_NOT_FOUND, detail=f"No location found for {name}")
        return loc_data

# async def get_person_location(engine, name: str, location: Annotated[Location, Depends(get_location_or_404)]):
#     """
#     Retrieve the location of a person by their name.

#     Args:
#         name (str): The name of the person.

#     Returns:
#         Location: The location of the person.
#     """
#     print(f"Fetching location for {name}")
    
#     print(f"Retrieved location data: {location}")
#     return location
