import pytest

from type_config import TypeConfig
from type_config.errors import ParsingError

class TestGetOption:
    get_option = TypeConfig()._get_option

    line = "my option = value"
    line_with_types = "[A type] my option = value"
    broken_line = "my option | value"
    empty_line = ""
    line_without_value = "my option ="

    def test_line(self):
        assert self.get_option(self.line) == ("my option", "value")

    def test_type_line(self):
        assert self.get_option(self.line_with_types) == ("my option", "value")

    def test_line_without_value(self):
        assert self.get_option(self.line_without_value) == ("my option", "")

    def test_broken_line(self):
        with pytest.raises(ParsingError):
            self.get_option(self.broken_line)

    def test_empty_line(self):
        with pytest.raises(ParsingError):
            self.get_option(self.empty_line)





