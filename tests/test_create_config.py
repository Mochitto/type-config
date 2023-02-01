from type_config import TypeConfig

class TestInputOutput:
    config = TypeConfig()
    
    formatted_output =(
            "test = value\n"
            "# !!! The test must pass\n"
            "# A test option\n"
            "\n"
            "test2 = \n"
            "# A test option"
            )

    formatted_output_with_type = (
            "[TestType] test = value\n"
            "# !!! The test must pass\n"
            "# A test option\n"
            "\n"
            "[TestType] test2 = \n"
            "# A test option"
            )

    result_config = {
            "test": "Test passed",
            }
    result_error = {"test2": "[test2]: can't be left empty."}

    formatted_input_with_corrupted = (
            "[TestType] test value\n"
            "test = value\n"
            "test | value                 "
            )
    corrupted_result = {
            "test": "Test passed"
            }
    corrupted_result_error = {
            "[TestType] test value" : "A broken line has been found.",
            "test | value" : "A broken line has been found."
            }

    def setup_class(self):
        self.config.add_option(
                option="test",
                type="TestType",
                help="A test option",
                default="value",
                important_help="The test must pass"
                )
        self.config.add_option(
                option="test2",
                type="TestType",
                help="A test option",
                )
        self.config.add_type(
                type="TestType",
                validate=lambda x: x == "value",
                cast=lambda x: "Test passed",
                error="The test value was not 'value'"
                )
    
    def test_create(self):
        assert self.config.create_config() == self.formatted_output

    def test_create_with_types(self):
        assert self.config.create_config(format_with_types=True) == self.formatted_output_with_type

    def test_parsing(self):
        assert self.config.parse_config(self.formatted_output) == (self.result_config, self.result_error)

    def test_parsing_with_types(self):
        assert self.config.parse_config(self.formatted_output_with_type) == (self.result_config, self.result_error)

    def test_corrupted_lines(self):
        assert self.config.parse_config(self.formatted_input_with_corrupted) == (self.corrupted_result, self.corrupted_result_error)



