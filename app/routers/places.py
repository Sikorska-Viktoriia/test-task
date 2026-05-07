from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..models import TravelProject, ProjectPlace
from ..schemas import PlaceCreate, PlaceResponse, PlaceUpdate
from ..services.artic_api import get_artwork
from ..services.project_service import update_project_completion

router = APIRouter(prefix="/projects", tags=["places"])


@router.post("/{project_id}/places", response_model=PlaceResponse)
def add_place(project_id: int, place: PlaceCreate, db: Session = Depends(get_db)):

    project = db.query(TravelProject).filter_by(id=project_id).first()

    if not project:
        raise HTTPException(404, "Project not found")

    count = db.query(ProjectPlace).filter_by(project_id=project_id).count()
    if count >= 10:
        raise HTTPException(400, "Max 10 places allowed")

    existing = db.query(ProjectPlace).filter_by(
        project_id=project_id,
        external_id=place.external_id
    ).first()

    if existing:
        raise HTTPException(400, "Place already exists")

    artwork = get_artwork(place.external_id)
    if not artwork:
        raise HTTPException(404, "Artwork not found in external API")

    new_place = ProjectPlace(
        project_id=project_id,
        external_id=place.external_id,
        title=artwork["title"],
        visited=False,
        notes=None
    )

    db.add(new_place)

    update_project_completion(db, project)

    db.commit()
    db.refresh(new_place)

    return new_place


@router.get("/{project_id}/places", response_model=list[PlaceResponse])
def get_places(project_id: int, db: Session = Depends(get_db)):

    project = db.query(TravelProject).filter_by(id=project_id).first()

    if not project:
        raise HTTPException(404, "Project not found")

    return project.places


@router.patch("/{project_id}/places/{place_id}", response_model=PlaceResponse)
def update_place(project_id: int, place_id: int, payload: PlaceUpdate, db: Session = Depends(get_db)):

    place = db.query(ProjectPlace).filter_by(
        id=place_id,
        project_id=project_id
    ).first()

    if not place:
        raise HTTPException(404, "Place not found")

    if payload.notes is not None:
        place.notes = payload.notes

    if payload.visited is not None:
        place.visited = payload.visited

    project = place.project
    update_project_completion(db, project)

    db.commit()
    db.refresh(place)

    return place


@router.get("/{project_id}/places/{place_id}", response_model=PlaceResponse)
def get_place(project_id: int, place_id: int, db: Session = Depends(get_db)):

    place = db.query(ProjectPlace).filter_by(
        id=place_id,
        project_id=project_id
    ).first()

    if not place:
        raise HTTPException(404, "Place not found")

    return place