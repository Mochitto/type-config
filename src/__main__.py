from typing import Tuple, List, Dict, Any
import re

from config_types.cast import cast_myList, cast_ExistingPath, cast_int, cast_myType
from config_types.validate import validate_MyList, validate_ExistingPath, validate_int, validate_MyType

import project_types.EasyConfig_types as ty
import project_types.EasyConfig_errors as er

class EasyConfig:
    def __init__(self, config_file: ty.Path) -> None:
        self.config = dict()
        self.file_path = config_file
        self._options_types = {}

    def _clean_file(self, file_content: str) -> str:
        cleaned_content = []
        for line in file_content.splitlines():
            line = line.strip()
            # Remove empty lines and comments 
            if line == "" or line.startswith("#"):
                continue
            if line.startswith("["):
                cleaned_content.append(line)
            else:
                pass
                #TODO: add error or ignore?
        return "\n".join(cleaned_content)

    def _get_option(self, line: str) -> Tuple[str, str, str]:
        type, result1 = line.split("]", 1)
        option, value = result1.split("=", 1)
        if not line.startswith("["):
            raise er.ParsingError(
                "Found broken line that has a malformed type.\n"+
                f"Info: {type}] {option} = {value}")
        return (type[1:].strip(), option.strip(), value.strip())

    def parse_file(self) -> Tuple[Dict[str, Any], List[str]]:    
        file_content = self._get_file_content()
        cleaned_file = self._clean_file(file_content)

        config = {}
        errors = []
        for line in cleaned_file.splitlines():
            try:
                type, option, value = self._get_option(line)
                is_valid = self._options_types[type]["validate"](value)
                if is_valid:
                    config[option] = self._options_types[type]["cast"](value)
            except er.ParsingError as err:
                errors.append(str(err))
                continue

        return (config, errors)

    def _get_file_content(self) -> str:
        with open(self.file_path, "r") as test_file:
            content = test_file.read()
        return content

    def add_type(self, type, validate, cast):
        self._options_types[type] = {
                "validate": validate,
                "cast": cast
                }

my_config = EasyConfig("config.mochi")
my_config.add_type("int", validate_int, cast_int)
my_config.add_type("MyType", validate_MyType, cast_myType)
my_config.add_type("MyList", validate_MyList, cast_myList)
my_config.add_type("ExistingPath", validate_ExistingPath, cast_ExistingPath)
print(my_config.parse_file())
