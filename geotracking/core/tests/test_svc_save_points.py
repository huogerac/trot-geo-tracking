import pytest
from time import sleep
from django.db.models import Count

from geotracking.core.models import Track, Circuit, Point
from geotracking.core.service import tracks_svc


@pytest.mark.django_db
def test_deve_salvar_pontos():
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

    # Chunk1
    p1 = {
        "dateTime": "2024-06-05T03:14:45.731108+00:00",
        "point": "p1",
        "longitude": -45.9094004,
        "latitude": -23.2432624,
    }
    p2 = {
        "dateTime": "2024-06-05T03:14:45.731109+00:00",
        "point": "p2",
        "longitude": -45.9094056,
        "latitude": -23.2432674,
    }
    p3 = {
        "dateTime": "2024-06-05T03:14:45.731110+00:00",
        "point": "p3",
        "longitude": -45.9094112,
        "latitude": -23.2432722,
    }
    p4 = {
        "dateTime": "2024-06-05T03:14:45.731111+00:00",
        "point": "p4",
        "longitude": -45.9094122,
        "latitude": -23.2432724,
    }
    p5 = {
        "dateTime": "2024-06-05T03:14:45.731112+00:00",
        "point": "p5",
        "longitude": -45.9094138,
        "latitude": -23.243277,
    }
    p6 = {
        "dateTime": "2024-06-05T03:14:45.731113+00:00",
        "point": "p6",
        "longitude": -45.9094146,
        "latitude": -23.2432819,
    }

    # Chunk 2  TRUE
    p7 = {
        "dateTime": "2024-06-05T03:14:45.731114+00:00",
        "point": "p7",
        "longitude": -45.909414,
        "latitude": -23.243283,
    }

    p8 = {
        "dateTime": "2024-06-05T03:14:45.731115+00:00",
        "point": "p8",
        "longitude": -45.909426,
        "latitude": -23.2432945,
    }

    p9 = {
        "dateTime": "2024-06-05T03:14:45.731116+00:00",
        "point": "p9",
        "longitude": -45.9094272,
        "latitude": -23.2432982,
    }

    # Chunk 3
    p10 = {
        "dateTime": "2024-06-05T03:14:45.731117+00:00",
        "point": "p10",
        "longitude": -45.9094287,
        "latitude": -23.2433031,
    }
    p11 = {
        "dateTime": "2024-06-05T03:14:45.731118+00:00",
        "point": "p11",
        "longitude": -45.9094287,
        "latitude": -23.2433031,
    }

    p12 = {
        "dateTime": "2024-06-05T03:14:45.731119+00:00",
        "point": "p12",
        "longitude": -45.9094311,
        "latitude": -23.2433085,
    }

    p13 = {
        "dateTime": "2024-06-05T03:14:45.731120+00:00",
        "point": "p13",
        "longitude": -45.9094311,
        "latitude": -23.2433085,
    }

    p14 = {
        "dateTime": "2024-06-05T03:14:45.731121+00:00",
        "point": "p14",
        "longitude": -45.909439367108064,
        "latitude": -23.243318557129385,
    }

    p15 = {
        "dateTime": "2024-06-05T03:14:45.731122+00:00",
        "point": "p15",
        "longitude": -45.90944322276442,
        "latitude": -23.24332579659996,
    }

    p16 = {
        "dateTime": "2024-06-05T03:14:45.731123+00:00",
        "point": "p16",
        "longitude": -45.909456897751426,
        "latitude": -23.243335111329145,
    }

    track = tracks_svc.start_track("Corrida 1", parque.id)

    tracks_svc.save_points(
        track.get("id"),
        [
            p1,
            p2,
            p3,
            p4,
            p5,
        ],
        MIN_TURN_POINTS=4,
        MIN_TURN_SEC=0,
    )
    sleep(1)
    tracks_svc.save_points(
        track.get("id"),
        [p6, p7, p8, p9, p10, p11],
        MIN_TURN_POINTS=4,
        MIN_TURN_SEC=0,
    )
    # Tem que iniciar Volta 2
    tracks_svc.save_points(
        track.get("id"),
        [p11, p12, p13, p14, p15, p16, p3, p4],
        MIN_TURN_POINTS=4,
        MIN_TURN_SEC=0,
    )
    tracks_svc.save_points(
        track.get("id"),
        [p7, p8, p9, p10, p11],
        MIN_TURN_POINTS=4,
        MIN_TURN_SEC=0,
    )
    tracks_svc.stop_track(parque.id)

    results = (
        Point.objects.filter(track_id=track.get("id"), ignored=False)
        .values("turn")
        .annotate(count=Count("turn"))
    )
    volta1, volta2 = results

    # assert results == {'turn': 1, 'count': 14}, {'turn': 2, 'count': 5}
    assert volta1 == {"turn": 1, "count": 14}
    assert volta2 == {"turn": 2, "count": 5}
