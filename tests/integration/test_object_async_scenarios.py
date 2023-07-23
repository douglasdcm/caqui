from caqui.synchronous import (
    find_element,
    get_session,
    click,
    send_keys,
    get_text,
    close_session,
    go_to_page,
    get_property,
    clear_element,
    get_rect,
    get_css_value,
    get_attribute,
    switch_to_frame,
    switch_to_parent_frame,
    dismiss_alert,
)
from tests.constants import PAGE_URL
from pytest import fixture, mark
from caqui.caqui import AsyncDriver


@fixture
def __setup():
    remote = "http://127.0.0.1:9999"
    capabilities = {
        "desiredCapabilities": {
            "browserName": "chrome",
            "acceptInsecureCerts": True,
            "goog:chromeOptions": {"extensions": [], "args": ["--headless"]},
        }
    }
    driver = AsyncDriver(remote, capabilities)
    yield driver
    driver.quit()


@mark.asyncio
async def test_switch_to_parent_frame_and_click_alert(__setup: AsyncDriver):
    driver = __setup
    await driver.get(PAGE_URL)

    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert_parent = "alert-button"
    locator_value_alert_frame = "alert-button-iframe"

    element_frame = await driver.find_element(locator_type, locator_value)
    assert await driver.switch_to.frame(element_frame) is True

    alert_button_frame = await driver.find_element(
        locator_type, locator_value_alert_frame
    )
    assert await alert_button_frame.click() is True
    assert await driver.switch_to.alert.dismiss() is True

    assert await driver.switch_to.default_content() is True
    alert_button_parent = await driver.find_element(
        locator_type, locator_value_alert_parent
    )
    assert await alert_button_parent.get_attribute("any") == "any"
    assert await alert_button_parent.click() is True


@mark.asyncio
async def test_switch_to_frame_and_click_alert(__setup: AsyncDriver):
    driver = __setup
    await driver.get(PAGE_URL)
    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert = "alert-button-iframe"

    element_frame = await driver.find_element(locator_type, locator_value)
    assert await driver.switch_to.frame(element_frame) is True

    alert_button = await driver.find_element(locator_type, locator_value_alert)
    assert await alert_button.get_attribute("any") == "any"
    assert await alert_button.click() is True


@mark.asyncio
async def test_get_data_from_hidden_button(__setup: AsyncDriver):
    driver = __setup
    locator_type = "xpath"
    await driver.get(PAGE_URL)

    hidden_button = await driver.find_element(locator_type, "//*[@id='hidden-button']")

    assert "width" in await hidden_button.get_rect()
    assert "visible" == await hidden_button.get_css_value("visibility")
    assert True is await hidden_button.get_property("hidden")
    assert ["display"] == await hidden_button.get_property("style")
    assert "display: none;" == await hidden_button.get_attribute("style")


@mark.asyncio
async def test_add_text__click_button_and_get_properties(__setup: AsyncDriver):
    driver = __setup
    expected = "end"
    locator_type = "xpath"
    await driver.get(PAGE_URL)

    input_ = await driver.find_element(locator_type, "//input")
    await input_.send_keys("any")
    assert await input_.get_property("value") == "any"
    await input_.clear()
    assert await input_.get_property("value") == ""

    anchor = await driver.find_element(locator_type, "//a")
    assert await anchor.get_property("href") == "http://any1.com/"

    button = await driver.find_element(locator_type, "//button")
    await button.click()

    p = await driver.find_element(locator_type, "//p[@id='end']")

    assert await p.get_text() == expected
