import pytest
from django.urls import reverse
from django.test import Client


@pytest.mark.django_db
def test_homepage():
    c = Client()
    response = c.get("/")
    assert response.status_code == 200
