import pytest
from time import sleep
from django.db.models import Count

from geotracking.core.models import Track, Circuit, Point
from geotracking.core.service import tracks_svc


@pytest.mark.django_db
def test_deve_savar_ignorar_pontos(client):
    # Dado um usuario logado
    # DADO

    points = [
        {
            "speed": 0.22,
        },
    ]
    payload = {"points": points}

    # Quando adicionamos um item
    resp = client.post(
        f"/api/core/tracks/000/points/save", payload, content_type="application/json"
    )
    msg = resp.json()

    # Entao
    assert resp.status_code == 422  # BAD REQUEST
    assert msg == {
        "message": "[INVALID INPUT] body.points.points.latitude: Field required (missing)",
    }


@pytest.mark.django_db
def test_deve_savar_2_pontos(client):
    # Dado um usuario logado
    # DADO
    parque = Circuit(
        name="Parque",
        start_line={
            "type": "LineString",
            "coordinates": [
                [-45.90952349700288, -23.243244069960497],
                [-45.9094043466919, -23.24329284597276],
            ],
        },
    )
    parque.save()
    track = tracks_svc.start_track("Corrida 1", parque.id)

    points = [
        {
            "dateTime": "2024-06-05T03:14:45.731116+00:00",
            "latitude": -23.2450982196426,
            "longitude": -45.909680847988795,
            "speed": 0.22,
        },
        {
            "dateTime": "2024-06-05T03:14:44.731117+00:00",
            "latitude": -23.244422035823774,
            "longitude": -45.909466359368764,
            "speed": 0.22,
        },
    ]
    payload = {"points": points}

    # Quando adicionamos um item
    resp = client.post(
        f"/api/core/tracks/{track.get('id')}/points/save",
        payload,
        content_type="application/json",
    )

    # Entao
    assert resp.status_code == 201
    assert resp.json() == {
        "result": {
            "points_saved": 2,
            "points_ignored": 2,
            "current_turn": 1,
        }
    }
