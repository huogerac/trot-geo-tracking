# coding: utf-8
import logging

from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt


from ninja import Router

from .schemas import (
    ListCircuitsSchema,
    TrackSchema,
    TrackSchemaIn,
    ListPointsSchema,
    ListTracksSchema,
    ListPointsSchemaOut,
)
from .service import tracks_svc

router = Router()
logger = logging.getLogger(__name__)


@router.get("/circuits", response=ListCircuitsSchema)
def list_circuits(request):
    """Lista Circuits"""
    logger.info("API list tracks")
    tracks = tracks_svc.list_circuits()
    return JsonResponse({"circuits": tracks})


@router.get("/tracks", response=ListTracksSchema)
def list_tracks(request):
    """Lista Tracks"""
    logger.info("API list tracks")
    tracks = tracks_svc.list_tracks()
    return JsonResponse({"tracks": tracks})


@router.get("/tracks/{track_id}/points", response=ListPointsSchemaOut)
def list_points(request, track_id: int):
    """Lista Tracks"""
    points = tracks_svc.list_points_compact(track_id)
    return JsonResponse({"points": points})


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
    saved, ignored, current_turn = tracks_svc.save_points(track_id, points.points)
    return JsonResponse(
        {
            "result": {
                "points_saved": saved,
                "points_ignored": ignored,
                "current_turn": current_turn,
            }
        },
        status=201,
    )


@router.post("/tracks/{track_id}/stop")
@csrf_exempt
def stop_track(request, track_id: int):
    result = tracks_svc.stop_track(track_id)
    return JsonResponse({"result": result})


@router.get("/tracks/{track_id}/download")
@csrf_exempt
def download_track_data(request, track_id: int):
    excel_file_output = tracks_svc.download_points(track_id)
    return FileResponse(open(excel_file_output, "rb"), as_attachment=True)
