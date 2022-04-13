from unittest.mock import MagicMock

import pytest

from dao.model.director import Director
from dao.model.genre import Genre
from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)
    movie1 = Movie(
        id=1,
        title="Movie1",
        description="description1",
        trailer="trailer1",
        year=2001,
        rating=1
    )

    movie2 = Movie(
        id=2,
        title="Movie2",
        description="description2",
        trailer="trailer2",
        year=2002,
        rating=5
    )

    movie3 = Movie(
        id=3,
        title="Movie3",
        description="description3",
        trailer="trailer3",
        year=2003,
        rating=10
    )

    dict_obj = {1: movie1, 2: movie2, 3: movie3}

    movie_dao.get_one = MagicMock(side_effect=dict_obj.get)
    movie_dao.get_all = MagicMock(return_value=[movie1, movie2, movie3])
    movie_dao.create = MagicMock(return_value=Movie(id=4, title="Movie4"))
    movie_dao.delete = MagicMock(side_effect=dict_obj.pop)
    movie_dao.update = MagicMock()
    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        movie_new = {
            "title": "Movie4",
        }
        movie = self.movie_service.create(movie_new)
        assert movie.id is not None

    def test_update(self):
        movie_upd = {
            "id": 4,
            "description": "description4",
            "trailer": "trailer4",
            "year": 2004,
            "rating": 4,
            "genre_id": 4,
            "director_id": 4,
        }
        self.movie_service.update(movie_upd)

    def test_delete(self):
        self.movie_service.delete(1)
        movie = self.movie_service.get_one(1)
        assert movie is None

    def test_partially_update(self):
        movie_upd = {
            "id": 3,
            "description": "description5",
        }
        self.movie_service.partially_update(movie_upd)
        movie = self.movie_service.get_one(movie_upd["id"])
        assert movie.description == "description5"

