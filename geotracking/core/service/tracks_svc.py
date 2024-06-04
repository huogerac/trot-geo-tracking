import logging

from ..models import Track
from geotracking.base.exceptions import BusinessError

logger = logging.getLogger(__name__)


def add_track(new_track: str) -> dict:
    logger.info("SERVICE add new track")
    if not isinstance(new_track, str):
        raise BusinessError("Invalid description")

    if not new_track or not new_track.strip():
        raise BusinessError("Invalid description")

    track = Track(description=new_track)
    track.save()
    logger.info("SERVICE track created.")
    return track.to_dict_json()


def list_tracks():
    logger.info("SERVICE list tracks")
    tracks_list = Track.objects.all()
    return [item.to_dict_json() for item in tracks_list]
