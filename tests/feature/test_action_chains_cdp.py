import time
from pytest import mark, raises

from caqui.by import By
from caqui.easy.cdp.drivers import AsyncDriver
from caqui.exceptions import WebDriverError


class TestCDPActionsChains:
    # @mark.asyncio
    # async def test_cdp_click(self, setup_cdp_playground: AsyncDriver):
    #     driver = setup_cdp_playground
    #     element = await driver.find_element(By.ID, "button")
    #     await driver.actions.click(element).perform()
    #     assert await element.get_css_value("color") == 'red'

    @mark.asyncio
    async def test_cdp_move_to_element(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground

        dummy = await driver.find_element(By.CSS_SELECTOR, "#app>button")
        # assert await dummy.get_text() == 'Click'
        h2 = await driver.find_element(By.XPATH, "//h2[text()='Tooltips and Popovers']")
        x = await h2.describe_element()
        print(x)
        assert await h2.get_text() == "Tooltips and Popovers"
        tooltip = await driver.find_element(By.XPATH, "//div[@class='tooltip']")
        await driver.actions.scroll_to_element(h2).move_to_element(tooltip).perform()
        assert "This is a toolti" in await tooltip.get_text()

    # @mark.asyncio
    # async def test_cdp_click_without_move_to_element(self, setup_cdp_playground: AsyncDriver):
    #     driver = setup_cdp_playground
    #     element = await driver.find_element(By.CSS_SELECTOR, "#app>button")
    #     await driver.actions.click(element).perform()

    # @mark.asyncio
    # async def test_cdp_scroll_to_element(self, setup_cdp_playground: AsyncDriver):
    #     driver = setup_cdp_playground
    #     element = await driver.find_element(By.CSS_SELECTOR, "#app>button")
    #     await driver.actions.scroll_to_element(element).perform()
    #     await element.click()

    # @mark.asyncio
    # async def test_cdp_click_without_scroll_to_element(self, setup_cdp_playground: AsyncDriver):
    #     driver = setup_cdp_playground
    #     element = await driver.find_element(By.CSS_SELECTOR, "#app>button")
    #     await element.click()
