from pytest import mark

from caqui import asynchronous, synchronous


@mark.asyncio
async def test_get_all_links(setup_functional_environment):
    driver = setup_functional_environment
    locator_type = "xpath"
    anchors = []

    for i in range(4):
        i += 1
        locator_value = f"//a[@id='a{i}']"
        anchor = synchronous.find_element(driver.server_url, driver.session, locator_type, locator_value)
        anchors.append(anchor)
        assert await asynchronous.get_text(driver.server_url, driver.session, anchors[i - 1]) == f"any{i}.com"
