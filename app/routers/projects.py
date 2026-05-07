from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..models import TravelProject, ProjectPlace
from ..schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from ..services.artic_api import get_artwork
from ..services.project_service import update_project_completion

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):

    project = TravelProject(
        name=payload.name,
        description=payload.description,
        start_date=payload.start_date,
        completed=False
    )

    db.add(project)
    db.flush()  

    for place in payload.places:

        count = db.query(ProjectPlace).filter_by(project_id=project.id).count()
        if count >= 10:
            raise HTTPException(400, "Max 10 places allowed per project")

        existing = db.query(ProjectPlace).filter_by(
            project_id=project.id,
            external_id=place.external_id
        ).first()

        if existing:
            continue

        artwork = get_artwork(place.external_id)
        if not artwork:
            raise HTTPException(404, f"Artwork {place.external_id} not found")

        db.add(ProjectPlace(
            project_id=project.id,
            external_id=place.external_id,
            title=artwork["title"],
            visited=False,
            notes=None
        ))

    update_project_completion(db, project)
    db.commit()
    db.refresh(project)

    return project


@router.get("/", response_model=list[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return db.query(TravelProject).all()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):

    project = db.query(TravelProject).filter_by(id=project_id).first()

    if not project:
        raise HTTPException(404, "Project not found")

    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):

    project = db.query(TravelProject).filter_by(id=project_id).first()

    if not project:
        raise HTTPException(404, "Project not found")

    for k, v in payload.dict(exclude_unset=True).items():
        setattr(project, k, v)

    db.commit()
    db.refresh(project)

    return project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):

    project = db.query(TravelProject).filter_by(id=project_id).first()

    if not project:
        raise HTTPException(404, "Project not found")

    if any(p.visited for p in project.places):
        raise HTTPException(400, "Cannot delete project with visited places")

    db.delete(project)
    db.commit()

    return {"message": "Project deleted"}