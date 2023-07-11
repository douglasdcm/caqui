# All fake responses where collected from chromedriver responses


class Dictionary:
    def __init__(self, dictionary) -> None:
        self.dictionary = dictionary

    def json(self):
        return self.dictionary

    # used by sync functions
    def get(self, key, *args):
        return self.dictionary.get(key)


def dict_to_json(dictionary):
    class MockResponse:
        @property
        def status_code(self):
            return 200

        # used by async functions
        def get(self, argument, *args):
            return dictionary.get(argument)

        def json(self):
            return Dictionary(dictionary)

    return MockResponse()


DEFAULT = dict_to_json(
    {
        "sessionId": "4358a5b53794586af59678fc1653dc40",
        "status": 0,
        "value": {"ELEMENT": "0.8851292311864847-1"},
    }
)

FIND_ELEMENT = DEFAULT
SEND_KEYS = DEFAULT
CLICK = DEFAULT
CLOSE_SESSION = DEFAULT
GO_TO_PAGE = DEFAULT

GET_NAMED_COOKIE = dict_to_json(
    {
        "value": {
            "name": "username",
            "value": "John Doe",
            "path": "//home/user/fullpath",
            "domain": "",
            "secure": False,
            "httpOnly": False,
            "sameSite": "None",
        }
    }
)

GET_RECT = dict_to_json(
    {
        "sessionId": "a9d6e77726f3eda12e92b06b5066dbb4",
        "status": 0,
        "value": {"height": 23, "width": 183, "x": 10, "y": 9652.12},
    }
)

ACTIONS = dict_to_json(
    {"sessionId": "449dbd1df001e9a9e13b3bac5babe809", "status": 0, "value": "null"}
)

EXECUTE_SCRIPT = dict_to_json(
    {"sessionId": "9f4a4a9420663d0c0cc18957ab463b90", "status": 0, "value": "any"}
)

GET_PAGE_SOURCE = dict_to_json(
    {
        "sessionId": "e34234d1445ed6d4833370d1d8019282",
        "status": 0,
        "value": "<html><head><title>Sample page</title></head><body><h1>Basic page</h1></body></html>",
    }
)

GET_ALERT_TEXT = dict_to_json(
    {"sessionId": "171ba19c927e0b95e1a53dbbdcfcdc19", "status": 0, "value": "any warn"}
)

GET_WINDOW_RECTANGLE = dict_to_json(
    {
        "sessionId": "79e4bd950a886e0119e3760d201b059e",
        "status": 0,
        "value": {"height": 600, "width": 800, "x": 0, "y": 0},
    }
)

GET_ACTIVE_ELEMENT = DEFAULT

CLEAR_ELEMENT = dict_to_json(
    {"sessionId": "486fa32a9876b4519e149b39135edcb5", "status": 0, "value": None}
)

IS_ELEMENT_ENABLED = dict_to_json(
    {"sessionId": "e0e43cd1ce532b5aa62b6df0de11e3bd", "status": 0, "value": True}
)

GET_CSS_COLOR_VALUE = dict_to_json(
    {
        "sessionId": "e7f659e7183778e98ce9357051e40a47",
        "status": 0,
        "value": "rgba(0, 0, 0, 1)",
    }
)

IS_ELEMENT_SELECTED = dict_to_json(
    {"sessionId": "341d21063846141d2716d300652ddd81", "status": 0, "value": False}
)

GET_WINDOW_HANDLES = dict_to_json(
    {
        "sessionId": "b3f92cf70d734ecc6fcddbd88671998a",
        "status": 0,
        "value": ["2E55CCE389196328988ED244DAA52A5D"],
    }
)

CLOSE_WINDOW = dict_to_json(
    {"sessionId": "48399161591a0bc1dffaa2ff2d65aa0f", "status": 0, "value": []}
)

GET_WINDOW = dict_to_json(
    {
        "sessionId": "ce68162d420e9cb2b1617c2d1a800f85",
        "status": 0,
        "value": "845623CAE8115F2B60C9AE8596F13D94",
    }
)

GET_URL = dict_to_json(
    {
        "sessionId": "af67b8ef665d30a687f37365d229fb53",
        "status": 0,
        "value": "file:///html/playground.html",
    }
)
GET_TIMEOUTS = dict_to_json(
    {
        "sessionId": "10754c8ec2e19133235223f1914ea376",
        "status": 0,
        "value": {"implicit": 0, "pageLoad": 300000, "script": 30000},
    }
)


GET_STATUS = dict_to_json(
    {
        "value": {
            "build": {
                "version": "113.0.5672.63 (0e1a4471d5ae5bf128b1bd8f4d627c8cbd55f70c-refs/branch-heads/5672@{#912})"
            },
            "message": "ChromeDriver ready for new sessions.",
            "os": {"arch": "x86_64", "name": "Linux", "version": "5.4.0-150-generic"},
            "ready": True,
        },
        "status": "0",  # fake status fro mock purposes. Not present in real response
    }
)

GET_TITLE = dict_to_json(
    {
        "sessionId": "07b00b2e94be84920495d83890c82b60",
        "status": 0,
        "value": "Sample page",
    }
)

GET_COOKIES = dict_to_json(
    {
        "sessionId": "07b00b2e94be84920495d83890c82b60",
        "status": 0,
        "value": [],
    }
)


FIND_ELEMENTS = dict_to_json(
    {
        "sessionId": "9be93a374d185216134bf0c3fafee52e",
        "status": 0,
        "value": [
            {"ELEMENT": "C230605181E69CB2C4C36B8E83FE1245_element_1"},
            {"ELEMENT": "C230605181E69CB2C4C36B8E83FE1245_element_2"},
            {"ELEMENT": "C230605181E69CB2C4C36B8E83FE1245_element_3"},
        ],
    }
)

GET_PROPERTY_VALUE = dict_to_json(
    {
        "sessionId": "5be82d4cd17af92d7ea53a36900d78cb",
        "status": 0,
        "value": "any_value",
    }
)

GET_ATTRIBUTE_VALUE = dict_to_json(
    {
        "sessionId": "5be82d4cd17af92d7ea53a36900d78cb",
        "status": 0,
        "value": "any_value",
    }
)

GET_TEXT = dict_to_json(
    {"sessionId": "5be82d4cd17af92d7ea53a36900d78cb", "status": 0, "value": "any"}
)

GET_SESSION = dict_to_json(
    {
        "sessionId": "4358a5b53794586af59678fc1653dc40",
        "status": 0,
        "value": {
            "acceptInsecureCerts": True,
            "acceptSslCerts": True,
            "applicationCacheEnabled": False,
            "browserConnectionEnabled": False,
            "browserName": "chrome",
            "chrome": {
                "chromedriverVersion": "94.0.4606.41 (333e85df3c9b656b518b5f1add5ff246365b6c24-refs/branch-heads/4606@{#845})",
                "userDataDir": "/tmp/.com.google.Chrome.4zKpeQ",
            },
            "cssSelectorsEnabled": True,
            "databaseEnabled": False,
            "goog:chromeOptions": {"debuggerAddress": "localhost:43565"},
            "handlesAlerts": True,
            "hasTouchScreen": False,
            "javascriptEnabled": True,
            "locationContextEnabled": True,
            "mobileEmulationEnabled": False,
            "nativeEvents": True,
            "networkConnectionEnabled": False,
            "pageLoadStrategy": "normal",
            "platform": "Linux",
            "proxy": {},
            "rotatable": False,
            "setWindowRect": True,
            "strictFileInteractability": False,
            "takesHeapSnapshot": True,
            "takesScreenshot": True,
            "timeouts": {"implicit": 0, "pageLoad": 300000, "script": 30000},
            "unexpectedAlertBehaviour": "ignore",
            "version": "94.0.4606.54",
            "webStorageEnabled": True,
            "webauthn:extension:credBlob": True,
            "webauthn:extension:largeBlob": True,
            "webauthn:virtualAuthenticators": True,
        },
    }
)
