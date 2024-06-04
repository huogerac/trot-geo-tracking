# coding: utf-8
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from ninja import Router

from .schemas import ListTracksSchema, TrackSchema, TrackSchemaIn


from .service import tracks_svc


router = Router()

logger = logging.getLogger(__name__)


@router.post("/tracks/add", response={201: TrackSchema})
@csrf_exempt
def add_track(request, track: TrackSchemaIn):
    """Adiciona Track"""
    logger.info("API add new track.")
    new_track = tracks_svc.add_track(track.description)

    return JsonResponse(new_track, status=201)


@router.get("/tracks/list", response=ListTracksSchema)
def list_tracks(request):
    """Lista Tracks"""
    logger.info("API list tracks")
    tracks = tracks_svc.list_tracks()
    return JsonResponse({"tracks": tracks})
