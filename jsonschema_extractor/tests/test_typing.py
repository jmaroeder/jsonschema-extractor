import pytest
from datetime import datetime
from typing import Any, List, Set, Optional, Union
from jsonschema_extractor.typing_extractor import TypingExtractor
from jsonschema_extractor.typing_extractor import _is_union


@pytest.fixture
def typing_extractor():
    return TypingExtractor()


@pytest.mark.parametrize("inp, expected_output", [
    (int, {"type": "integer"}),
    (float, {"type": "number"}),
    (str, {"type": "string"}),
    (type(None), {"type": "null"}),
    (datetime, {"type": "string", "format": "date-time"}),
    (Optional[int], {
        "anyOf": [
            {"type": "integer"},
            {"type": "null"},
        ]
    }),
    (Union[int, str], {
        "anyOf": [
            {"type": "integer"},
            {"type": "string"},
        ]
    }),
    (List[int], {
        "type": "array",
        "items": {
            "type": "integer"
        }
    }),
])
def test_extract_typing(extractor, inp, expected_output):
    assert extractor.extract(inp) == expected_output


def test_typing_extractor_register(typing_extractor):

    class Foo(object):
        pass

    def extract_foo(extractor, typ):
        return {
            "type": "string",
        }

    typing_extractor.register(Foo, extract_foo)

    assert typing_extractor.extract(typing_extractor, Foo) == {
        "type": "string",
    }


def test_is_union():
    assert _is_union(Optional[int])
