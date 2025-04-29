from os import getcwd

BASE_DIR = getcwd()
ROOT_DIR = BASE_DIR + "/caqui/src"
TEST_DIR = BASE_DIR + "/tests"

PAGE_URL = f"file:///{TEST_DIR}/html/playground.html"
COOKIE = {
    "domain": ".example.org",
    "expiry": 1760687129,
    "httpOnly": True,
    "name": "NID",
    "path": "/",
    "sameSite": "Lax",
    "secure": True,
    "value": "523=Sc0_gsThISC9jkAfuOsEdaX51SxT6FWqrG3UWhn7eaw5JZooxNWC2jbQZVadDFgM4OYLjDSTAYPb3rQdKt23GQgDcTa_iuLSOyJ7Tlpo3PKa_ijrjrcoMeIWT6O6DnvvG1q8tSfeahhzv44f9cgkJrjZ5VPC4wg1ZKocrQFiJOZEIS6XZpsK73d2hnw0HZkTymQsYt3UVoWrsqPujsTzw542M45aSRl3U406lNMU9zailbJurvW6ZRVL2TIaaUMhkQ",  # noqa E501
}
