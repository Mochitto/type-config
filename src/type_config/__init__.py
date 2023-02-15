from typing import Tuple, Dict, Any

import type_config.errors as er


class TypeConfig:
    def __init__(self, type_hint=False) -> None:
        self._options_types = {}
        self._options = {}
        self.type_hint = type_hint

    def add_type(self, type, validate, cast, error):
        self._options_types[type] = {"validate": validate, "cast": cast, "error": error}

    def add_option(
        self,
        type: str,
        option: str,
        help: str,
        default="",
        can_be_empty=False,
        important_help="",
    ):
        self._options[option] = {
            "type": type,
            "option": option,
            "default": default,
            "can_be_empty": can_be_empty,
            "important_help": important_help,
            "help": help,
        }

    def get_options(self):
        return self._options.copy()

    def get_types(self):
        return self._options_types.copy()

    def _get_option(self, line: str) -> Tuple[str, str]:
        """
        Extract option and value from the given line.
        The type, if present, is ignored.
        """
        # Remove type
        if "]" in line:
            _, _, line = line.partition("]")

        # Remove inline comments 
        line = line.split("#")[0]

        option, equal_sign, value = line.partition("=")

        if not equal_sign or not option:
            raise er.ParsingError(f"A broken line has been found.")

        return (option.strip(), value.strip())

    def _clean_file(self, file_content: str) -> str:
        """
        Remove from the given string empty lines and
        lines with comments.
        """
        cleaned_content = []
        for line in file_content.splitlines():
            line = line.strip()
            # Remove empty lines and comments
            if line == "" or line.startswith("#"):
                continue
            cleaned_content.append(line)
        return "\n".join(cleaned_content)

    def _validate_option(self, option: str, value: str | None) -> Any:
        """
        Validate the given option's value.

        Raise an exception if:
            - The option is not part of the config's options
            - The option's type is not part of the config's types
            - A value that can't be empty is left empty
            - The value is invalid.
        """
        option_info = self._options.get(option, None)
        if not option_info:
            raise er.ValidationError(f"[{option}]: is not part of the expected options.")

        type = option_info["type"]
        default = option_info["default"]
        can_be_empty = option_info["can_be_empty"]

        if not value:
            value = default if default else None
        if not value and not can_be_empty:
            raise er.ValidationError(f"[{option}]: can't be left empty.")
        # Until here

        try:
            validating_func = self._options_types[type]["validate"]
            casting_func = self._options_types[type]["cast"]
        except KeyError:
            raise er.ValidationError(f"[{type}]: is not part of the expected types.")

        is_valid = validating_func(value)
        if is_valid:
            return casting_func(value)
        else:
            raise er.ValidationError(
                f"[{option}]: {self._options_types[type]['error']} (value: {value})"
            )

    def parse_config(self, file_content: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
        cleaned_file = self._clean_file(file_content)

        config = {}
        errors = {}
        for line in cleaned_file.splitlines():
            try:
                option, value = self._get_option(line)
            except er.ParsingError as err:
                errors[line.strip()] = str(err) 
                continue

            try:
                config[option] = self._validate_option(option, value)
            except er.ValidationError as err:
                errors[option] = str(err)
                continue

        return (config, errors)

    def validate_config(
        self, config: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """
        Validate a pre-existing dictionary containing all, or a part, of
        the TypeConfig's options.
        Return a tuple containing the validated data and
        a dictionary with the options that were not valid and their errors.
        """
        errors = dict()
        validated_config = dict()

        for option, value in config.items():
            try:
                validated_config[option] = self._validate_option(option, value)
            except er.ValidationError as err:
                errors[option] = str(err)

        return validated_config, errors

    def merge_config(
        self, overwriting_config: Dict[str, Any], overwritable_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge two configs and return a new dictionary containing
        the values obtained, without modifying the original configs nor
        validating their values.

        If an option is present in overwriting_config and its value is
        not null (or falsy), overwrite the overwritable_config's option's value.

        If the value is null in both, attempt to use a default.
        If the value is still null and it can't be empty, an exception
        is raised.
        """
        result_config = {}
        options = set([*overwriting_config.keys(), *overwritable_config.keys()])

        for option in options:
            option_info = self._options.get(option, None)
            if not option_info:
                raise er.ParsingError(
                    f"[{option}]: is not part of the expected options."
                )

            result_value = None
            overwriting_value = overwriting_config.get(option, None)
            overwrited_value = overwritable_config.get(option, None)
            default_value = option_info["default"]
            can_be_empty = option_info["can_be_empty"]

            if overwriting_value is not None:
                result_value = overwriting_value
            elif overwrited_value is not None:
                result_value = overwrited_value
            elif default_value:
                result_value = default_value
            elif can_be_empty:
                result_value = None
            else:
                raise er.ParsingError(f"[{option}]: can't be left empty")

            result_config[option] = result_value

        return result_config

    def _formatter(self, option_info, add_type=False):
        help = "\n".join([f"# {line}" for line in option_info["help"].splitlines()]) 
        important_help = "\n".join([f"# !!! {line}" for line in option_info["important_help"].splitlines()]) 

        result = (
            "[{type}] {option} = {default}\n" if add_type else "{option} = {default}\n"
        )
        result += f"{important_help}\n" if important_help else ""
        result += help
        return result.format(**option_info)

    def create_config(self) -> str:
        """
        Return a formatted string that can be written to a file
        with your configuration's options, values and comments.
        """
        options_to_write = []
        for option_info in self._options.values():
            options_to_write.append(
                self._formatter(option_info, self.type_hint)
            )

        return "\n\n".join(options_to_write)

    def heal_config(self, file_content: str) -> str:
        """
        Restore the config file when corrupted.
        If an {option: value} pair isn't corrupted,
        the value is stored and the user's configuration
        retained, else the default value is used.
        """
        cleaned_file = self._clean_file(file_content)

        config = dict()
        for line in cleaned_file.splitlines():
            value = None
            if line.count("=") > 1:
                continue
            option, value = self._get_option(line)
            config[option] = value

        options_to_write = []
        for option_info in self._options.values():
            option = option_info["option"]
            # Overwriting the stored info gives a new default
            # to maintain the existing values
            if option in config and config[option]:
                option_info["default"] = config[option]

            options_to_write.append(
                self._formatter(option_info, self.type_hint)
            )

        return "\n\n".join(options_to_write)
