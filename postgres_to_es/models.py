from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from typing import Optional, List


class EntityMixin(BaseModel):
    id: UUID


class FilmParticipant(EntityMixin):
    name: str


class Movie(EntityMixin):
    title: str
    imdb_rating: Optional[float] = None
    genre: Optional[List[str]] = None
    description: Optional[str] = None
    director: Optional[List[str]] = []
    actors_names: Optional[List[str]] = []
    writers_names: Optional[List[str]] = []
    actors: Optional[List[FilmParticipant]] = []
    writers: Optional[List[FilmParticipant]] = []
