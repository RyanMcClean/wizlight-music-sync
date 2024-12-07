import pytest
import random, string
from bulbControlFrontend.models import wizbulb


@pytest.fixture
def testName():
    class TestName:
        def get(self):
            letters = string.ascii_letters
            return "".join(random.choice(letters) for i in range(random.randrange(50)))

    return TestName()


@pytest.fixture
def testIp():
    class TestIp:
        def get(self):
            numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            return "".join(random.choice(numbers) for i in range(15))

    return TestIp()


@pytest.mark.django_db
def test_db_creation(testName, testIp):
    testNums = 1000
    nameList = []
    ipList = []
    stateList = []
    redList = []
    blueList = []
    greenList = []
    tempList = []
    while len(nameList) < testNums:
        name = testName.get()
        if name not in nameList:
            nameList.append(name)

    while len(ipList) < testNums:
        ip = testIp.get()
        if ip not in ipList:
            ipList.append(ip)

    for i in range(testNums):
        stateList.append(bool(random.getrandbits(1)))
        redList.append(random.randrange(255))
        greenList.append(random.randrange(255))
        blueList.append(random.randrange(255))
        tempList.append(random.randrange(100))

    for name, ip, state, red, green, blue, temp in zip(
        nameList, ipList, stateList, redList, greenList, blueList, tempList
    ):
        wizbulb.objects.create(
            bulbName=name, bulbIp=ip, bulbState=state, bulbRed=red, bulbGreen=green, bulbBlue=blue, bulbTemp=temp
        )
        testBulb = wizbulb.objects.get(bulbName=name)
        assert testBulb.bulbName == name
        assert testBulb.bulbIp == ip
        assert testBulb.bulbState == state
        assert testBulb.bulbRed == red
        assert testBulb.bulbGreen == green
        assert testBulb.bulbBlue == blue
        assert testBulb.bulbTemp == temp
