from caqui.helper import get_elements
from pytest import mark
from tests.fake_responses import FIND_ELEMENTS


@mark.parametrize(
    "response,expected",
    [
        (
            {
                "value": [
                    {
                        "element-6066-11e4-a52e-4f735466cecf": "c4cab128-a0a4-4355-93a5-ffd6c7a8b042"
                    },
                    {
                        "element-6066-11e4-a52e-4f735466cecf": "12345678-a0a4-4355-93a5-ffd6c7a8b042"
                    },
                ]
            },
            [
                "c4cab128-a0a4-4355-93a5-ffd6c7a8b042",
                "12345678-a0a4-4355-93a5-ffd6c7a8b042",
            ],
        ),
        (
            FIND_ELEMENTS,
            [
                "C230605181E69CB2C4C36B8E83FE1245_element_1",
                "C230605181E69CB2C4C36B8E83FE1245_element_2",
                "C230605181E69CB2C4C36B8E83FE1245_element_3",
            ],
        ),
    ],
)
def test_get_elements(response, expected):
    assert get_elements(response) == expected
