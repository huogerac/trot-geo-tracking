import logging
from shapely.geometry import shape, Polygon, Point
from django.db.models import Max
from django.utils import timezone

from geotracking.base.exceptions import BusinessError
from ..models import Track, Circuit
from ..models import Point as PointModel

logger = logging.getLogger(__name__)


def list_circuits():
    logger.info("SERVICE list circuits")
    circuits_list = Circuit.objects.all()
    return [item.to_dict_json() for item in circuits_list]


def start_track(description: str, circuit_id: int) -> dict:
    circuit = Circuit.objects.filter(id=circuit_id).first()
    if not circuit:
        raise BusinessError("Invalid Circuit: id ", circuit_id)

    track = Track(description=description, circuit=circuit)
    track.save()
    logger.info("Track created.")
    return track.to_dict_json()


def stop_track(track_id: int) -> dict:
    track = Track.objects.filter(id=track_id).first()
    if not track:
        raise BusinessError("Invalid Track: id ", track_id)
    track.finished = True
    return track.to_dict_json()


def save_points(track_id: int, points, MIN_TURN_SEC=10, MIN_TURN_POINTS=42):
    track = Track.objects.filter(id=track_id).first()
    if not track:
        raise BusinessError("Invalid Track: id ", track_id)

    start_line = Polygon(shape(track.circuit.start_line))

    # { "latitude": -28.5048571, "longitude": -49.0151939, "latLongAccuracy": 19.214000701904297,
    #  "heading": null, "speed": null, "altitude": 7.099999904632568, "altitudeAccuracy": null,
    #  "date": 1675385450042 }

    saved = 0
    ignored = 0
    for item in points:
        point_data = item.get("point_data")
        local_date = point_data.get("dateTime")

        point = Point(
            shape(
                {
                    "type": "Point",
                    "coordinates": [
                        point_data.get("longitude"),
                        point_data.get("latitude"),
                    ],
                }
            )
        )

        # Descarta ponto, se não passou pela linha de início
        cross_start_line = point.intersects(start_line)
        if not track.started and not cross_start_line:
            ignored += 1
            continue

        current_turn = (
            PointModel.objects.filter(track_id=track_id)
            .values("turn")
            .aggregate(max=Max("turn"))["max"]
            or 1
        )

        if cross_start_line:
            if not track.started:
                track.started = True
                track.save()

            current_saved_points = PointModel.objects.filter(
                track_id=track_id, turn=current_turn
            ).count()

            first_saved_point = (
                PointModel.objects.filter(track_id=track_id, turn=current_turn)
                .order_by("id")
                .first()
            )

            seconds_last_saved = 0
            if first_saved_point:
                seconds_last_saved = (
                    timezone.now() - first_saved_point.created_at
                ).seconds

            new_turn = (
                seconds_last_saved > MIN_TURN_SEC
                and current_saved_points > MIN_TURN_POINTS
            )
            if new_turn:
                current_turn += 1

        new_point = PointModel(
            track=track,
            turn=current_turn,
            point_data=point_data,
            created_at_local=local_date,
        )
        new_point.save()
        saved += 1

    return (saved, ignored)
