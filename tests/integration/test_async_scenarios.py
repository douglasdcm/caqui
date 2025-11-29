from caqui import synchronous, asynchronous
from pytest import mark


@mark.asyncio
async def test_get_all_links(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = "xpath"
    anchors = []

    for i in range(4):
        i += 1
        locator_value = f"//a[@id='a{i}']"
        anchor = synchronous.find_element(server_url, session, locator_type, locator_value)
        anchors.append(anchor)
        assert await asynchronous.get_text(server_url, session, anchors[i - 1]) == f"any{i}.com"
