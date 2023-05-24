import aiohttp
import json
from caqui.constants import HEADERS
from caqui.exceptions import WebDriverError


async def __post(url, payload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=HEADERS) as resp:
                response = await resp.json()
                return response
    except Exception as error:
        raise WebDriverError("'POST' request failed.") from error


async def get_property_value(driver_url, session, element):
    try:
        url = f"{driver_url}/session/{session}/element/{element}/property/value"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS) as resp:
                response = await resp.json()
                return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get value from element.") from error


async def get_text(driver_url, session, element):
    try:
        url = f"{driver_url}/session/{session}/element/{element}/text"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS) as resp:
                response = await resp.json()
                return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get text from element.") from error


async def close_session(driver_url, session):
    try:
        url = f"{driver_url}/session/{session}"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=HEADERS) as resp:
                response = await resp.json()
                return response.get("sessionId")
    except Exception as error:
        raise WebDriverError("Failed to close session.") from error


async def go_to_page(driver_url, session, page_url):
    try:
        url = f"{driver_url}/session/{session}/url"
        payload = json.dumps({"url": page_url})
        response = await __post(url, payload)
        return response.get("sessionId")
    except Exception as error:
        raise WebDriverError(f"Failed to navigate to page '{page_url}'.") from error


async def send_keys(driver_url, session, element, text):
    try:
        url = f"{driver_url}/session/{session}/element/{element}/value"
        payload = json.dumps({"text": text, "value": [*text], "id": element})
        response = await __post(url, payload)
        return response.get("sessionId")
    except Exception as error:
        raise WebDriverError(f"Failed to send key '{text}'.") from error


async def click(driver_url, session, element):
    try:
        payload = json.dumps({"id": element})
        url = f"{driver_url}/session/{session}/element/{element}/click"
        response = await __post(url, payload)
        return response.get("sessionId")
    except Exception as error:
        raise WebDriverError("Failed to click on element.") from error


async def find_element(driver_url, session, locator_type, locator_value):
    try:
        payload = json.dumps({"using": locator_type, "value": locator_value})
        url = f"{driver_url}/session/{session}/element"
        response = await __post(url, payload)
        return response.get("value").get("ELEMENT")
    except Exception as error:
        raise WebDriverError(
            f"Failed to find element by '{locator_type}'-'{locator_value}'."
        ) from error


async def get_session(driver_url, capabilities):
    try:
        payload = json.dumps(capabilities)
        url = f"{driver_url}/session"
        response = await __post(url, payload)
        return response.get("sessionId")
    except Exception as error:
        raise WebDriverError("Failed to open session.") from error
