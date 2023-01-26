from typing import Tuple, List, Dict, Any, Set

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

    def _get_option(self, line: str) -> Tuple[str, str]:
        # TODO: could still leave in the bit to recognize the type
        # and leave it as a formatting choice
        option, _, value = line.partition("=")
        return (option.strip(), value.strip())

    def parse_file(self) -> Tuple[Dict[str, Any], List[str]]:  
        # TODO: might use a special error for missing types
        file_content = self._get_file_content()
        cleaned_file = self._clean_file(file_content)

        config = {}
        errors = []
        for line in cleaned_file.splitlines():
            option, value = self._get_option(line)
            # TODO: this part could be its own "get_option"
            # and do the whole default etc on its own
            # with a try except
            option_info = self._options.get(option, None)
            if not option_info: 
                errors.append(f"[{option}]: is not part of the expected options.")
                continue

            type = option_info["type"]
            default = option_info["default"]
            is_optional = option_info["optional"]

            if not value:
                value = default if default else None
            if not value and not is_optional:
                errors.append(f"[{option}]: was left blank, but needs a value.")
                continue
            # Until here

            try:
                is_valid = self._options_types[type]["validate"](value)
                if is_valid:
                    config[option] = self._options_types[type]["cast"](value)
                else: 
                    errors.append(f"[{option}]: {self._options_types[type]['error']} (value: {value})")
            except er.ParsingError as err:
                errors.append(str(err))
                continue
        return (config, errors)

    def heal_file(self) -> None:
        """
        Restore the config file when corrupted.
        If an option: value pair isn't corrupted,
        the value is stored and the user's configuration
        maintained, else, the default value is used.
        """
        file_content = self._get_file_content()
        cleaned_file = self._clean_file(file_content)
        
        config = dict()
        for line in cleaned_file.splitlines():
            value = None
            option, value = self._get_option(line) 
            config[option] = value
        
        options_to_write = []
        for option_info in self._options.values():
            option = option_info["option"]
            if option in config and config[option]:
                option_info["default"] = config[option]

            options_to_write.append(self._formatter(option_info))
        
        with open(self.file_name, "w") as config_file:
            config_file.write("\n".join(options_to_write))

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

        result = "{option} = {default}\n"
        result += "# !!! {constraints}\n" if constraints else ""
        result += "# {help}\n"
        return result.format(**option_info)

    def write_config(self) -> None:
        options_to_write = []
        for option_info in self._options.values():
            options_to_write.append(self._formatter(option_info))

        with open(self.file_name, "w") as config_file:
            config_file.write("\n".join(options_to_write))

    def validate_config(self, config: Dict[str, Any])-> Tuple[Dict[str, Any], Set[str]]:
        """
        Validate a pre-existing dictionary containing all, or a part, of 
        the EasyConfig's options.
        Return a tuple containing the validated data and 
        a set with the options that were not valid.
        """
        bad_options = set()
        validated_config = dict() 

        for option, value in config.items():
            try:
                option_info = self._options[option]
            except KeyError as err:
                raise er.ParsingError(f"[{option}]: is not an expected option.") from err

            type = option_info["type"]
            validating_func = self._options_types[type]["validate"]
            casting_func = self._options_types[type]["cast"]

            default = option_info["default"]
            is_optional = option_info["optional"]

            if not value:
                value = default if default else None
            if not value and not is_optional:
                raise er.ParsingError(f"[{option}]: was left blank, but needs a value.")

            is_valid = validating_func(value)
            if is_valid:
                validated_config[option] = casting_func(value)
            else:
                bad_options.add(option)

        return validated_config, bad_options

