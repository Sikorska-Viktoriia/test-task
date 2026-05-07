from sqlalchemy.orm import Session
from ..models import TravelProject


def update_project_completion(db: Session, project: TravelProject):
    project.completed = (
        len(project.places) > 0 and all(p.visited for p in project.places)
    )