from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db

from ..models import TravelProject, ProjectPlace
from ..schemas import PlaceCreate, PlaceResponse, PlaceUpdate
from ..services.artic_api import get_artwork

router = APIRouter(
    prefix="/projects",
    tags=["Places"]
)


def update_project_completion(project: TravelProject):
    if not project.places:
        project.completed = False
    else:
        project.completed = all(place.visited for place in project.places)


@router.post("/{project_id}/places", response_model=PlaceResponse)
async def add_place(
    project_id: int,
    place: PlaceCreate,
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

    if len(project.places) >= 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 places allowed"
        )


    existing_place = db.query(ProjectPlace).filter(
        ProjectPlace.project_id == project_id,
        ProjectPlace.external_id == place.external_id
    ).first()

    if existing_place:
        raise HTTPException(
            status_code=400,
            detail="Place already exists in project"
        )


    artwork = await get_artwork(place.external_id)

    if not artwork:
        raise HTTPException(
            status_code=404,
            detail="Artwork not found in Art Institute API"
        )

    new_place = ProjectPlace(
        project_id=project_id,
        external_id=artwork["external_id"],
        title=artwork["title"],
        visited=False
    )

    db.add(new_place)
    db.commit()
    db.refresh(new_place)

    update_project_completion(project)
    db.commit()

    return new_place


@router.get("/{project_id}/places", response_model=list[PlaceResponse])
def get_places(
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

    return project.places



@router.get("/{project_id}/places/{place_id}", response_model=PlaceResponse)
def get_place(
    project_id: int,
    place_id: int,
    db: Session = Depends(get_db)
):

    place = db.query(ProjectPlace).filter(
        ProjectPlace.id == place_id,
        ProjectPlace.project_id == project_id
    ).first()

    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    return place


@router.patch("/{project_id}/places/{place_id}", response_model=PlaceResponse)
def update_place(
    project_id: int,
    place_id: int,
    data: PlaceUpdate,
    db: Session = Depends(get_db)
):

    place = db.query(ProjectPlace).filter(
        ProjectPlace.id == place_id,
        ProjectPlace.project_id == project_id
    ).first()

    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    if data.notes is not None:
        place.notes = data.notes

    if data.visited is not None:
        place.visited = data.visited

    db.commit()
    db.refresh(place)


    project = db.query(TravelProject).filter(
        TravelProject.id == project_id
    ).first()

    update_project_completion(project)
    db.commit()

    return place