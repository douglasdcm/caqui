from caqui.by import By
from caqui import synchronous
from pytest import mark


@mark.parametrize(
    "locator, value",
    [
        (By.CLASS_NAME, "my-class"),
        (By.CSS_SELECTOR, ".my-class"),
        (By.ID, "button"),
        (By.LINK_TEXT, "any2.com"),
        (By.NAME, "fname"),
        (By.PARTIAL_LINK_TEXT, "any3"),
        (By.TAG_NAME, "input"),
        (By.XPATH, "//button"),
    ],
)
def test_locators(setup_functional_environment, locator, value):
    server_url, session = setup_functional_environment
    assert synchronous.find_element(server_url, session, locator, value) is not None
