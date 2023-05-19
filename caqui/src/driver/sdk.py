import requests
import json

HEADERS = {
    "Accept-Encoding": "identity",
    "Accept": "application/json",
    "Content-Type": "application/json;charset=UTF-8",
    "Connection": "keep-alive",
}


def __get(url, payload):
    return requests.request("GET", url, headers=HEADERS, data=payload).json()


def __post(url, payload):
    return requests.request("POST", url, headers=HEADERS, data=payload).json()


def __delete(url):
    return requests.request("DELETE", url, headers={}, data={}).json()


def __get_session(response):
    return response.get("sessionId")


def get_property_value(driver_url, session, element):
    url = f"{driver_url}/session/{session}/element/{element}/property/value"
    response = __get(url, {})
    return response.get("value")


def go_to_page(driver_url, session, page_url):
    url = f"{driver_url}/session/{session}/url"
    payload = json.dumps({"url": page_url})
    response = __post(url, payload)
    return __get_session(response)


def close_session(driver_url, session):
    url = f"{driver_url}/session/{session}"
    response = __delete(url)
    return __get_session(response)


def get_text(driver_url, session, element):
    url = f"{driver_url}/session/{session}/element/{element}/text"
    response = __get(url, {})
    return response.get("value")


def send_keys(driver_url, session, element, text):
    url = f"{driver_url}/session/{session}/element/{element}/value"
    payload = json.dumps({"text": text, "value": [*text], "id": element})
    response = __post(url, payload)
    return __get_session(response)


def click(driver_url, session, element):
    url = f"{driver_url}/session/{session}/element/{element}/click"
    payload = json.dumps({"id": element})
    response = __post(url, payload)
    return __get_session(response)


def get_session(driver_url, capabilities):
    url = f"{driver_url}/session"
    response = __post(url, capabilities)
    return __get_session(response)


def find_element(driver_url, session, locator_type, locator_value):
    url = f"{driver_url}/session/{session}/element"
    payload = json.dumps({"using": locator_type, "value": locator_value})
    response = __post(url, payload)
    return response.get("value").get("ELEMENT")
