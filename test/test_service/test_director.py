from unittest.mock import MagicMock

import pytest

from dao.model.director import Director
from dao.director import DirectorDAO
from service.director import DirectorService


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)
    director1 = Director(
        id=1,
        name="Director1"
    )

    director2 = Director(
        id=2,
        name="Director2"
    )

    director3 = Director(
        id=3,
        name="Director3"
    )

    dict_obj = {1: director1, 2: director2, 3: director3}

    director_dao.get_one = MagicMock(side_effect=dict_obj.get)
    director_dao.get_all = MagicMock(return_value=[director1, director2, director3])
    director_dao.create = MagicMock(return_value=Director(id=4, name="Director4"))
    director_dao.delete = MagicMock(side_effect=dict_obj.pop)
    director_dao.update = MagicMock()
    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0

    def test_create(self):
        director_new = {
            "name": "Director4",
        }
        director = self.director_service.create(director_new)
        assert director.id is not None

    def test_update(self):
        director_upd = {
            "id": 3,
            "name": "Director_upd",
        }
        self.director_service.partially_update(director_upd)
        director = self.director_service.get_one(director_upd["id"])
        assert director.name == "Director_upd"

    def test_delete(self):
        self.director_service.delete(1)
        director = self.director_service.get_one(1)
        assert director is None

