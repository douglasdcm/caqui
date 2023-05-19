class Dictionary:
    def __init__(self, dictionary) -> None:
        self.dictionary = dictionary

    def json(self):
        return self.dictionary

    def get(self, key):
        return self.dictionary.get(key)


def dict_to_json(dictionary):
    return Dictionary(dictionary)


DEFAULT = dict_to_json(
    {
        "sessionId": "4358a5b53794586af59678fc1653dc40",
        "status": 0,
        "value": {"ELEMENT": "0.8851292311864847-1"},
    }
)

FIND_ELEMENT = DEFAULT
GET_URL = DEFAULT
SEND_KEYS = DEFAULT
CLICK = DEFAULT
CLOSE_SESSION = DEFAULT
GO_TO_PAGE = DEFAULT

GET_PROPERTY_VALUE = dict_to_json(
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
