import pytest
import requests
from time import sleep

from bulbControlFrontend.views import index


@pytest.mark.django_db
def test_index(live_server):
    response = requests.get(live_server.url + "/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_index_view(rf):
    request = rf.get("")
    response = index(request)
    assert response.status_code == 200
