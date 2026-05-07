from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base


class TravelProject(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False)

    places = relationship(
        "ProjectPlace",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class ProjectPlace(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    external_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)

    notes = Column(Text, nullable=True)
    visited = Column(Boolean, default=False)

    project = relationship("TravelProject", back_populates="places")