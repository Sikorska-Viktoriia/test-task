from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import TravelProject
from ..schemas import ProjectCreate
from ..schemas import ProjectResponse
from ..schemas import ProjectUpdate
from ..dependencies import get_db

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):

    new_project = TravelProject(
        name=project.name,
        description=project.description,
        start_date=project.start_date
    )

    db.add(new_project)

    db.commit()

    db.refresh(new_project)

    return new_project


@router.get("/", response_model=list[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db)
):

    return db.query(TravelProject).all()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = db.query(TravelProject).filter(
        TravelProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    updated_data: ProjectUpdate,
    db: Session = Depends(get_db)
):

    project = db.query(TravelProject).filter(
        TravelProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if updated_data.name is not None:
        project.name = updated_data.name

    if updated_data.description is not None:
        project.description = updated_data.description

    if updated_data.start_date is not None:
        project.start_date = updated_data.start_date

    db.commit()

    db.refresh(project)

    return project

@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = db.query(TravelProject).filter(
        TravelProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    visited_places = any(
        place.visited for place in project.places
    )

    if visited_places:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete project with visited places"
        )

    db.delete(project)

    db.commit()