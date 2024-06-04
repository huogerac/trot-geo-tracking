import pytest
from unittest.mock import ANY

from geotracking.core.models import Track


def test_nao_deve_permitir_listar_track_sem_login(client):
    # Dado um usuário anônimo

    # Quando tentamos listar itens
    resp = client.get("/api/core/tracks/list")

    # Entao recebemos um sem autorizacao
    assert resp.status_code == 401


@pytest.mark.django_db
def test_deve_retornar_lista_vazia(client, logged_jon):
    # Quando tentamos listar itens
    resp = client.get("/api/core/tracks/list")
    data = resp.json()

    # Entao recebemos um sem autorizacao
    assert resp.status_code == 200
    assert data.get("tracks") == []


@pytest.mark.django_db
def test_deve_listar_track_com_login(client, logged_jon):
    # Dado um item criado
    Track.objects.create(description="walk the dog")

    # Quando listamos
    resp = client.get("/api/core/tracks/list")
    data = resp.json()

    # Entao
    assert resp.status_code == 200
    assert data == {
        "tracks": [{"description": "walk the dog", "done": False, "id": ANY}]
    }
