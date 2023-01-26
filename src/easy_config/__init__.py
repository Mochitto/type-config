from typing import Tuple, List, Dict, Any

import easy_config.EasyConfig_types as ty
import easy_config.EasyConfig_errors as er

class EasyConfig:
    def __init__(self, file_name: ty.Path) -> None:
        self.file_name = file_name
        self._options_types = {}
        self._options = {}

    def _clean_file(self, file_content: str) -> str:
        cleaned_content = []
        for line in file_content.splitlines():
            line = line.strip()
            # Remove empty lines and comments 
            if line == "" or line.startswith("#"):
                continue
            cleaned_content.append(line)
        return "\n".join(cleaned_content)

    def _get_option(self, line: str) -> Tuple[str, str, str]:
        type, result1 = line.split("]", 1)
        option, value = result1.split("=", 1)
        if not line.startswith("["):
            raise er.ParsingError(
                "Found broken line that has a malformed type. "+
                f"(Line: {type}] {option} = {value})")
        return (type[1:].strip(), option.strip(), value.strip())

    def parse_file(self) -> Tuple[Dict[str, Any], List[str]]:  
        # TODO: might use a special error for missing types
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
                else: 
                    errors.append(f"{option}: {self._options_types[type]['error']} (value: {value})")
            except er.ParsingError as err:
                errors.append(str(err))
                continue
        return (config, errors)

    def _get_file_content(self) -> str:
        with open(self.file_name, "r") as test_file:
            content = test_file.read()
        return content

    def add_type(self, type, validate, cast, error):
        self._options_types[type] = {
                "validate": validate,
                "cast": cast,
                "error": error
                }

    def add_option(
            self,
            type: str, 
            option: str,
            help: str,
            **kwargs):
        default = kwargs.get("default", "")
        optional = kwargs.get("optional", False)
        constraints = kwargs.get("constraints", "")
        self._options[option] = {
                "type": type,
                "option": option,
                "default": default,
                "optional": optional,
                "constraints": constraints,
                "help": help
                }

    def _formatter(self, option_info):
        constraints = option_info["constraints"]

        result = "[{type}] {option} = {default}\n"
        result += "# !!! {constraints}\n" if constraints else ""
        result += "# {help}\n"
        return result.format(**option_info)

    def write_config(self) -> None:
        options_to_write = []
        for option in self._options.values():
            options_to_write.append(self._formatter(option))

        with open(self.file_name, "w") as config_file:
            config_file.write("\n".join(options_to_write))
