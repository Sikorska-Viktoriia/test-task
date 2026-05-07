# Travel Planner API

A RESTful backend service for managing travel projects and places to visit.  
Built with FastAPI, SQLAlchemy, and integrated with the Art Institute of Chicago API for external data validation.

## Overview

This application allows users to create travel projects and manage collections of places associated with each project.  
Each place is validated against an external API before being stored.

A project represents a travel plan and consists of multiple places. Users can update place information, mark places as visited, and track overall project completion status.

## Features

### Travel Projects
- Create a travel project with name, description, and optional start date
- Retrieve a list of all projects
- Retrieve a single project by ID
- Update project details
- Delete a project with business constraint:
  - A project cannot be deleted if any associated place is marked as visited


### Project Places
- Add a place to a project using an external API validation step
- Support importing multiple places during project creation
- Retrieve all places within a project
- Retrieve a single place within a project
- Update place details:
  - Notes
  - Visited status

## Business Rules

- Maximum of 10 places per project
- Duplicate places within the same project are not allowed
- Each place must exist in the Art Institute of Chicago API before being added
- A project is considered completed when all associated places are marked as visited
- Deletion of a project is blocked if any place is marked as visited

## External API Integration

The system uses the Art Institute of Chicago API to validate places before storing them.

API endpoint:
https://api.artic.edu/api/v1/artworks

Each place is identified by an external ID and must exist in the external system.


## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- httpx
- Docker
- Docker Compose

## Project Structure


app/
├── routers/ API route handlers
├── models/ Database models (SQLAlchemy)
├── schemas/ Request and response schemas (Pydantic)
├── services/ Business logic and external API integration
├── database.py Database configuration
├── dependencies.py Dependency injection (DB session)
└── main.py Application entry point



## Running the Application

### Using Docker

Build and run the application:

```bash
docker-compose up --build

API documentation will be available at:

http://localhost:8000/docs
Local Setup

Install dependencies:

pip install -r requirements.txt

Run the server:

uvicorn app.main:app --reload
API Endpoints
Projects
- POST /projects/ — Create a project
- GET /projects/ — Get all projects
- GET /projects/{project_id} — Get project by ID
- PATCH /projects/{project_id} — Update project
- DELETE /projects/{project_id} — Delete project

Places
- POST /projects/{project_id}/places — Add place to project
- GET /projects/{project_id}/places — Get all places in project
- GET /projects/{project_id}/places/{place_id} — Get single place
- PATCH /projects/{project_id}/places/{place_id} — Update place

Limitations
- SQLite is used as the database (not production-ready)
- No authentication or authorization implemented
- No pagination for list endpoints
- No caching layer for external API requests
- No automated tests included

Possible Improvements
- Replace SQLite with PostgreSQL
- Add authentication (JWT-based)
- Implement caching for external API responses
- Add pagination and filtering for list endpoints
- Add unit and integration tests
- Improve architecture with service/repository separation