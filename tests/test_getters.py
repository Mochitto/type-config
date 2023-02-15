from type_config import TypeConfig

class TestInputOutput:
    config = TypeConfig()

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
                cast=lambda _: "Test passed",
                error="The test value was not 'value'"
                )
    
    def test_get_options(self):
        assert self.config.get_options() == self.config._options

    def test_get_types(self):
        assert self.config.get_types() == self.config._options_types
