import pytest

from bulbControlFrontend.models import wizbulb


@pytest.fixture
def setUpVars():
    return {
        "testName": "test bulb",
        "testIp": "192.168.50.252",
        "testState": False,
        "testRed": 0,
        "testGreen": 0,
        "testBlue": 0,
        "testTemp": 0,
    }


@pytest.fixture
def setUp(setUpVars):
    print("Set Up")
    wizbulb.objects.create(
        bulbName=setUpVars["testName"],
        bulbIp=setUpVars["testIp"],
        bulbState=setUpVars["testState"],
        bulbRed=setUpVars["testRed"],
        bulbGreen=setUpVars["testGreen"],
        bulbBlue=setUpVars["testBlue"],
        bulbTemp=setUpVars["testTemp"],
    )
    yield setUpVars
    print("Teardown")
    wizbulb.objects.get(bulbName=setUpVars["testName"]).delete()


@pytest.mark.django_db
def test_db_creation(setUp):
    testBulb = wizbulb.objects.get(bulbName=setUp["testName"])
    assert testBulb.bulbName == setUp["testName"]
    assert testBulb.bulbIp == setUp["testIp"]
    assert testBulb.bulbState == setUp["testState"]
    assert testBulb.bulbRed == setUp["testRed"]
    assert testBulb.bulbGreen == setUp["testGreen"]
    assert testBulb.bulbBlue == setUp["testBlue"]
    assert testBulb.bulbTemp == setUp["testTemp"]


def test_addition():
    assert 2 - 1 == 1
