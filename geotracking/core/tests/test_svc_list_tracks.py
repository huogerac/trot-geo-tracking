import pytest

from geotracking.core.models import Track
from geotracking.core.service import tracks_svc


@pytest.mark.django_db
def test_deve_retornar_lista_vazia():
    itens_list = tracks_svc.list_tracks()
    assert itens_list == []


@pytest.mark.django_db
def test_deve_listar_com_10_iten():
    # Dado 10 itens criados
    itens = [Track(description=f"Tracks nro ${number}") for number in range(1, 11)]
    Track.objects.bulk_create(itens)

    itens_list = tracks_svc.list_tracks()

    assert len(itens_list) == 10
