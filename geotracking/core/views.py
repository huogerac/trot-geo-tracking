# coding: utf-8
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from ninja import Router

from .schemas import ListCircuitsSchema, TrackSchema, TrackSchemaIn, ListPointsSchema
from .service import tracks_svc

router = Router()
logger = logging.getLogger(__name__)


@router.get("/circuits", response=ListCircuitsSchema)
def list_circuits(request):
    """Lista Tracks"""
    logger.info("API list tracks")
    tracks = tracks_svc.list_circuits()
    return JsonResponse({"circuits": tracks})


@router.post("/tracks/start", response={201: TrackSchema})
@csrf_exempt
def start_track(request, track: TrackSchemaIn):
    """Adiciona novo percurso"""
    logger.info("API add new track.")
    new_track = tracks_svc.start_track(track.description, track.circuit_id)
    return JsonResponse(new_track, status=201)


@router.post("/tracks/{track_id}/points/save", response={201: dict})
@csrf_exempt
def save_points(request, track_id: int, points: ListPointsSchema):
    saved, ignored = tracks_svc.save_points(track_id, points.points)
    return JsonResponse(
        {
            "result": {
                "points_saved": saved,
                "points_ignored": ignored,
            }
        },
        status=201,
    )


@router.post("/tracks/{track_id}/stop")
@csrf_exempt
def stop_track(request, track_id: int):
    result = tracks_svc.stop_track(track_id)
    return JsonResponse({"result": result})
