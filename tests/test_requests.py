import pytest
import requests
from time import sleep


@pytest.mark.live_server
@pytest.mark.django_db
def test_index(live_server):
    sleep(20)
    url = live_server.url
    response = requests.get(live_server.url)
    assert response.status_code == 200
