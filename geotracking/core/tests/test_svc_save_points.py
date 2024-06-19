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

    # Chunk1
    p1 = {
        "date": "2024-06-05T03:14:45.731108+00:00",
        "point": "p1",
        "point_data": {
            "latitude": -23.243319063161948,
            "longitude": -45.909546770165974,
        },
    }
    p2 = {
        "date": "2024-06-05T03:14:45.731109+00:00",
        "point": "p2",
        "point_data": {"latitude": -23.24338014651329, "longitude": -45.90955479349145},
    }
    p3 = {
        "date": "2024-06-05T03:14:45.731110+00:00",
        "point": "p3",
        "point_data": {"latitude": -23.243415954036223, "longitude": -45.9095559398192},
    }
    p4 = {
        "date": "2024-06-05T03:14:45.731111+00:00",
        "point": "p4",
        "point_data": {
            "latitude": -23.243409635072382,
            "longitude": -45.909612103098226,
        },
    }
    p5 = {
        "date": "2024-06-05T03:14:45.731112+00:00",
        "point": "p5",
        "point_data": {"latitude": -23.24345808045733, "longitude": -45.90958688693189},
    }
    p6 = {
        "date": "2024-06-05T03:14:45.731113+00:00",
        "point": "p6",
        "point_data": {
            "latitude": -23.243578604040266,
            "longitude": -45.90965570664031,
        },
    }

    # Chunk 2
    p7 = {
        "date": "2024-06-05T03:14:45.731114+00:00",
        "point": "p7",
        "point_data": {
            "latitude": -23.244956101412384,
            "longitude": -45.910454820869916,
        },
    }

    p8 = {
        "date": "2024-06-05T03:14:45.731115+00:00",
        "point": "p8",
        "point_data": {"latitude": -23.245248183642744, "longitude": -45.910083567573},
    }

    p9 = {
        "date": "2024-06-05T03:14:45.731116+00:00",
        "point": "p9",
        "point_data": {"latitude": -23.2450982196426, "longitude": -45.909680847988795},
    }

    p10 = {
        "date": "2024-06-05T03:14:45.731117+00:00",
        "point": "p10",
        "point_data": {
            "latitude": -23.244422035823774,
            "longitude": -45.909466359368764,
        },
    }
    p11 = {
        "date": "2024-06-05T03:14:45.731118+00:00",
        "point": "p11",
        "point_data": {
            "latitude": -23.243817288552492,
            "longitude": -45.90931875489193,
        },
    }

    # Chunk 3
    p12 = {
        "date": "2024-06-05T03:14:45.731119+00:00",
        "point": "p12",
        "point_data": {"latitude": -23.2429805048166, "longitude": -45.909117786213216},
    }

    p13 = {
        "date": "2024-06-05T03:14:45.731120+00:00",
        "point": "p13",
        "point_data": {
            "latitude": -23.242943433000633,
            "longitude": -45.90933908444052,
        },
    }

    p14 = {
        "date": "2024-06-05T03:14:45.731121+00:00",
        "point": "p14",
        "point_data": {
            "latitude": -23.243067093456446,
            "longitude": -45.909409917766226,
        },
    }

    p15 = {
        "date": "2024-06-05T03:14:45.731122+00:00",
        "point": "p15",
        "point_data": {
            "latitude": -23.243203770668856,
            "longitude": -45.909466584427406,
        },
    }

    p16 = {
        "date": "2024-06-05T03:14:45.731123+00:00",
        "point": "p16",
        "point_data": {
            "latitude": -23.243377743139916,
            "longitude": -45.909586335564796,
        },
    }

    track = tracks_svc.start_track("Corrida 1", parque.id)

    tracks_svc.save_points(track.get("id"), [p1, p2, p3, p4, p5, p6])
    sleep(1)
    tracks_svc.save_points(track.get("id"), [p7, p8, p9, p10, p11])
    # Tem que iniciar Volta 2
    tracks_svc.save_points(
        track.get("id"),
        [p11, p12, p13, p14, p15, p16, p3, p4],
        MIN_TURN_POINTS=10,
        MIN_TURN_SEC=0,
    )
    tracks_svc.save_points(track.get("id"), [p7, p8, p9, p10, p11])
    tracks_svc.stop_track(parque.id)

    results = (
        Point.objects.filter(track_id=track.get("id"))
        .values("turn")
        .annotate(count=Count("turn"))
    )
    volta1, volta2 = results

    assert volta1 == {"turn": 1, "count": 15}
    assert volta2 == {"turn": 2, "count": 7}
