from pydantic import BaseModel, ConfigDict
from datetime import date



class PlaceCreate(BaseModel):
    external_id: int


class PlaceUpdate(BaseModel):
    notes: str | None = None
    visited: bool | None = None


class PlaceResponse(BaseModel):
    id: int
    project_id: int
    external_id: int
    title: str
    visited: bool
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)



class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    start_date: date | None = None
    places: list[PlaceCreate] = []


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: date | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    start_date: date | None = None
    completed: bool
    places: list[PlaceResponse] = []

    model_config = ConfigDict(from_attributes=True)