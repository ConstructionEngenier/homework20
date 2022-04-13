from unittest.mock import MagicMock

import pytest

from dao.model.genre import Genre
from dao.genre import GenreDAO
from service.genre import GenreService


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(None)
    genre1 = Genre(
        id=1,
        name="Genre1"
    )

    genre2 = Genre(
        id=2,
        name="Genre2"
    )

    genre3 = Genre(
        id=3,
        name="Genre3"
    )

    dict_obj = {1: genre1, 2: genre2, 3: genre3}

    genre_dao.get_one = MagicMock(side_effect=dict_obj.get)
    genre_dao.get_all = MagicMock(return_value=[genre1, genre2, genre3])
    genre_dao.create = MagicMock(return_value=Genre(id=4, name="Genre4"))
    genre_dao.delete = MagicMock(side_effect=dict_obj.pop)
    genre_dao.update = MagicMock()
    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre is not None
        assert genre.id is not None

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) > 0

    def test_create(self):
        genre_new = {
            "name": "Genre4",
        }
        genre = self.genre_service.create(genre_new)
        assert genre.id is not None

    def test_update(self):
        genre_upd = {
            "id": 3,
            "name": "Genre_upd",
        }
        self.genre_service.partially_update(genre_upd)
        genre = self.genre_service.get_one(genre_upd["id"])
        assert genre.name == "Genre_upd"

    def test_delete(self):
        self.genre_service.delete(1)
        genre = self.genre_service.get_one(1)
        assert genre is None

