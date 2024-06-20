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
            "type": "Polygon",
            "coordinates": [
                [
                    [-45.90945979543875, -23.2434429978873],
                    [-45.90965464763198, -23.243360851343255],
                    [-45.90966152476821, -23.243394552495843],
                    [-45.90947125733206, -23.243468273736696],
                    [-45.90945979543875, -23.2434429978873],
                ]
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
            "points_saved": 0,
            "points_ignored": 2,
        }
    }
