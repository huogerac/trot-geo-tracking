import os
from django.db import connection
from django.http import JsonResponse
from .exceptions import BusinessError

from ninja import Router

from .schemas import Error

router = Router()


@router.get("/dapau", response={400: Error, 500: Error})
def dapau(request, error: str = None):
    """
    Retorna um erro real para ajudar nos testes
    """
    if error and error.upper() == "BUSINESS":
        raise BusinessError("BusinessError")
    raise Exception("break on purpose")


@router.get("/status", response={200: dict})
def status(request):
    """
    Retorna o estado atual da aplicação
    """
    cursor = connection.cursor()
    cursor.execute("""SELECT 1+1""")
    row = cursor.fetchone()
    git_hash = os.getenv("GIT_HASH", "?")
    return JsonResponse(
        {
            "status": "ok",
            "db": "ok" if row == (2,) else "error",
            "git_hash": git_hash,
        }
    )
