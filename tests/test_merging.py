import pytest

from type_config import TypeConfig
from type_config.errors import ParsingError

class TestInputOutput:
    config = TypeConfig()
    validate = config._validate_option

    overwriting = {
            "test": "value",
            "test3": None,
            "emptyTest": None
            }

    overwrited = {
            "test": None,
            "test2": "value2",
            "test3": "value3",
            "testDefault": None 
            }

    overwrited_result = {
            "test": "value",
            "test2": "value2",
            "test3": "value3",
            "emptyTest": None,
            "testDefault": "value4"
            }

    bad_overwrited_option = {
            "awalw": "102"
            }

    bad_overwriting_empty = {
            "test": None
            }

    overwriting_with_falsy = {
            "test": False,
            }

    overwrited_with_falsy = {
            "test": True,
            "test2": False
            }

    result_with_falsy = {
            "test": False,
            "test2": False
            }


    def setup_class(self):
        self.config.add_option(
                option="test",
                type="TestType",
                help="A test option",
                )
        self.config.add_option(
                option="test2",
                type="TestType",
                help="A test option",
                )
        self.config.add_option(
                option="test3",
                type="TestType",
                help="A test option",
                )
        self.config.add_option(
                option="emptyTest",
                type="TestType",
                help="A test option",
                can_be_empty=True
                )
        self.config.add_option(
                option="testDefault",
                type="TestType",
                help="A test option",
                default="value4"
                )

    def test_overwriting(self):
        assert self.config.merge_config(self.overwriting, self.overwrited) == self.overwrited_result

    def test_unknown_option(self):
        with pytest.raises(ParsingError):
            self.config.merge_config(self.bad_overwrited_option, self.overwrited)

    def test_bad_empty_value(self):
        with pytest.raises(ParsingError):
            self.config.merge_config(self.bad_overwriting_empty, self.overwrited)

    def test_falsy_values(self):
        assert self.config.merge_config(self.overwriting_with_falsy, self.overwrited_with_falsy) == self.result_with_falsy

