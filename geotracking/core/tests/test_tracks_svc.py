import pytest
from unittest.mock import MagicMock
from mock import patch
from django.utils import timezone
from ..service.tracks_svc import save_points
from ..models import Track
from ..models import Point as PointModel

from geotracking.base.exceptions import BusinessError


@pytest.fixture
def mock_track():
    track = MagicMock(spec=Track)
    track.circuit.start_line = {"type": "LineString", "coordinates": [[0, 0], [1, 1]]}
    track.started = False
    return track


@pytest.fixture
def mock_point_model():
    return MagicMock(spec=PointModel)


def test_save_points_invalid_track(mocker):
    mocker.patch(
        "geotracking.core.models.Track.objects.filter"
    ).return_value.first.return_value = None
    with pytest.raises(BusinessError):
        save_points(1, [])


def test_save_points_no_points(mocker, mock_track):
    mocker.patch(
        "geotracking.core.models.Track.objects.filter"
    ).return_value.first.return_value = mock_track
    saved, ignored, current_turn = save_points(1, [])
    assert saved == 0
    assert ignored == 0
    assert current_turn == 0
