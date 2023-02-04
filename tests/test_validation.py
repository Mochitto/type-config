import pytest

from type_config import TypeConfig
from type_config.errors import ValidationError

class TestInputOutput:
    config = TypeConfig()
    validate = config._validate_option

    # Passing
    config_good = ("test", "value")
    config_good_empty_value = ("emptyTest", "")
    config_default = ("testDefault", "")
    # Failing
    config_unknown_option = ("ayyy", "Test failed")
    config_unknown_type = ("test2", "Test failed")
    config_bad_empty_value = ("test", "")
    config_bad_value = ("test", "")

    existing_config = {
            "test": "value",
            "emptyTest": None
            }

    existing_config_err = {
            "test": None,
            "emptyTest": None
            }

    def setup_class(self):
        self.config.add_option(
                option="test",
                type="TestType",
                help="A test option",
                important_help="The test must pass"
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
                default="value"
                )
        self.config.add_option(
                option="test2",
                type="FakeType",
                help="A test option",
                )
        
        self.config.add_type(
                type="TestType",
                validate=lambda x: x == "value" or not x,
                cast=lambda x: "Test passed",
                error="The test value was not 'value'"
                )

    def test_validating_existing_config(self):
        assert self.config.validate_config(self.existing_config) == ({"test": "Test passed", "emptyTest": "Test passed"}, {})

    def test_validating_existing_config_err(self):
        assert self.config.validate_config(self.existing_config_err) == ({"emptyTest": "Test passed"}, {"test": "[test]: can't be left empty."})

    def test_config(self):
        assert self.validate(*self.config_good) == "Test passed"

    def test_good_empty(self):
        assert self.validate(*self.config_good_empty_value) == "Test passed"

    def test_default(self):
        assert self.validate(*self.config_default) == "Test passed"

    def test_unknown_error(self):
        with pytest.raises(ValidationError):
            self.validate(*self.config_unknown_option)

    def test_unknown_type(self):
        with pytest.raises(ValidationError):
            self.validate(*self.config_unknown_type)
    
    def test_bad_empty(self):
        with pytest.raises(ValidationError):
            self.validate(*self.config_bad_empty_value)

    def test_bad_value(self):
        with pytest.raises(ValidationError):
            self.validate(*self.config_bad_value)
