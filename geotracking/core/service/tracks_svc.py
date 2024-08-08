import logging
from shapely.geometry import shape, Point, LineString
from shapely import buffer
import pandas as pd

from django.db.models import Max
from django.utils import timezone
from django.db import connection
from geotracking.base.exceptions import BusinessError
from ..models import Track, Circuit
from ..models import Point as PointModel

logger = logging.getLogger(__name__)


def list_circuits():
    logger.info("SERVICE list circuits")
    circuits_list = Circuit.objects.all()
    return [item.to_dict_json() for item in circuits_list]


def list_tracks():
    tracks_list = Track.objects.filter(finished=True).order_by("-id")
    return [item.to_dict_json() for item in tracks_list]


def list_points(track_id):
    points = PointModel.objects.filter(track_id=track_id, ignored=False).order_by("id")
    return [item.to_dict_json() for item in points]


def list_points_compact(track_id):
    points = PointModel.objects.filter(track_id=track_id, ignored=False).order_by("id")
    return [
        {
            "id": item.id,
            "track_id": item.track_id,
            "turn": item.turn,
            "latitude": item.point_data.get("latitude"),
            "longitude": item.point_data.get("longitude"),
        }
        for item in points
    ]


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
    track.save()
    return track.to_dict_json()


def save_points(
    track_id: int, points, MIN_TURN_SEC=20, MIN_TURN_POINTS=42, BUFFER_SIZE=0.00001
):
    """
    Saves a collection of points in the following format:
    [
      {
        "latitude": -28.5048571, "longitude": -49.0151939, "latLongAccuracy": 19.214000701904297,
        "heading": null, "speed": null, "altitude": 7.099999904632568, "altitudeAccuracy": null,
        "dateTime": 1675385450042
      }
    ]
    """
    logger.info(f"Saving points: {len(points)}")
    track = Track.objects.filter(id=track_id).first()
    if not track:
        raise BusinessError("Invalid Track: id ", track_id)

    properties = track.circuit.start_line.get("properties", {})
    # start_line = Polygon(shape(track.circuit.start_line))
    start_line = LineString(shape(track.circuit.start_line))

    MIN_TURN_SEC = properties.get("MIN_TURN_SEC", MIN_TURN_SEC)
    MIN_TURN_POINTS = properties.get("MIN_TURN_POINTS", MIN_TURN_POINTS)
    BUFFER_SIZE = properties.get("BUFFER_SIZE", BUFFER_SIZE)

    current_turn = 0
    saved = 0
    total_ignored = 0
    for item in points:
        point_data = dict(item)
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
        ignored = False

        # Descarta ponto, se não passou pela linha de início
        point_buffer = buffer(point, distance=BUFFER_SIZE)
        cross_start_line = point_buffer.intersects(start_line)
        if not track.started and not cross_start_line:
            ignored = True
            total_ignored += 1

        current_turn = (
            PointModel.objects.filter(track_id=track_id)
            .values("turn")
            .aggregate(max=Max("turn"))["max"]
            or 1
        )

        if cross_start_line:
            logger.info(
                f"Crossed start line: lat:{point_data.get('latitude')} long:{point_data.get('longitude')}"
            )
            if not track.started:
                track.started = True
                track.save()

            current_saved_points = PointModel.objects.filter(
                track_id=track_id,
                turn=current_turn,
                ignored=False,
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
                logger.info(f"New Turn: {current_turn}")

        new_point = PointModel(
            track=track,
            turn=current_turn,
            point_data=point_data,
            ignored=ignored,
            created_at_local=local_date,
        )
        new_point.save()
        saved += 1

    logger.info(f"Saved: {saved}; Ignored: {total_ignored}")
    return (saved, total_ignored, current_turn)


def download_points(track_id):
    track = Track.objects.filter(id=track_id).first()
    if not track:
        raise BusinessError("Invalid Track: id ", track_id)

    query = """
    SELECT p.track_id, p.id, p.turn, p.ignored, p.created_at_local,
           p.point_data->>'latitude' as latitude,
           p.point_data->>'longitude' as longitude,
           p.point_data->>'latLongAccuracy' as latLongAccuracy,
           p.point_data->>'heading' as heading,
           p.point_data->>'speed' as speed
    FROM core_point as p
    ORDER BY p.id
    """

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    cols = [
        "track_id",
        "id",
        "turn",
        "ignored",
        "created_at_local",
        "latitude",
        "longitude",
        "latLongAccuracy",
        "heading",
        "speed",
    ]
    df = pd.DataFrame(rows, columns=cols)
    df["created_at_local"] = df["created_at_local"].dt.tz_localize(None)

    output_file_path = f"/tmp/track_data_{track_id}.xlsx"
    df.to_excel(output_file_path, sheet_name="Sheet1", index=False)
    return output_file_path
