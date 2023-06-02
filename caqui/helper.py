def get_elements(response):
    values = response.get("value")
    return [list(value.values())[0] for value in values]


def get_element(response):
    value = response.get("value")
    # Google Chrome
    element = value.get("ELEMENT")
    if element:
        return element

    # Firefox
    return list(value.values())[0]
