from pytest import mark

from caqui.by import By
from caqui.easy.drivers import AsyncDriver


@mark.parametrize("locator, value", [(By.ID, "shadow-button"), (By.CSS_SELECTOR, "button")])
@mark.asyncio
async def test_find_elements_from_shadow_root(setup_playground: AsyncDriver, locator, value):
    driver = setup_playground
    locator_type = By.ID
    locator_value = "shadow-root"
    expected = "Click Shadow"

    shadow_host = await driver.find_element(locator_type, locator_value)
    shadow_root = shadow_host.shadow_root
    shadow_content = await shadow_root.find_elements(locator, value)
    actual = await shadow_content[0].get_text()

    assert actual == expected


@mark.parametrize("locator, value", [(By.ID, "shadow-button"), (By.CSS_SELECTOR, "button")])
@mark.asyncio
async def test_find_element_from_shadow_root(setup_playground: AsyncDriver, locator, value):
    driver = setup_playground
    locator_type = By.ID
    locator_value = "shadow-root"
    expected = "Click Shadow"

    shadow_host = await driver.find_element(locator_type, locator_value)
    shadow_root = shadow_host.shadow_root
    shadow_content = await shadow_root.find_element(locator, value)
    actual = await shadow_content.get_text()

    assert actual == expected
