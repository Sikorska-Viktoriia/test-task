from pydantic import BaseModel
from datetime import date


class PlaceCreate(BaseModel):
    external_id: int


class PlaceUpdate(BaseModel):
    notes: str | None = None
    visited: bool | None = None


class PlaceResponse(BaseModel):
    id: int
    external_id: int
    title: str
    notes: str | None
    visited: bool

    class Config:
        from_attributes = True


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
    description: str | None
    completed: bool

    places: list[PlaceResponse] = []

    class Config:
        from_attributes = True