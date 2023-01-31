from type_config import TypeConfig

class TestInputOutput:
    config = TypeConfig()

    broken_config = """
    test4 = SOMETHING # Even added an inline comment
    # New order of options
    # I changed this comment because Yeah

    test2 = something else test = oof removed newline

    test3 = a value
    """

    healed_config = (
    "test = default value\n"
    "# !!! The test must pass\n"
    "# A test option\n"
    "\n"
    "test2 = \n"
    "# A test option\n"
    "\n"
    "test3 = a value\n"
    "# A test option\n"
    "\n"
    "test4 = SOMETHING\n"
    "# !!! Must be all caps\n"
    "# A test option"
    )

    broken_config_with_types = """
    [What's this???] test4 = SOMETHING # Even added an inline comment
    # New order of options
    # I changed this comment because Yeah

    [RandomType] test2 = something else test = oof removed newline

    test3 = a value
    """
    
    healed_config_with_types = (
    "[TestType] test = default value\n"
    "# !!! The test must pass\n"
    "# A test option\n"
    "\n"
    "[TestType] test2 = \n"
    "# A test option\n"
    "\n"
    "[TestType] test3 = a value\n"
    "# A test option\n"
    "\n"
    "[TestType] test4 = SOMETHING\n"
    "# !!! Must be all caps\n"
    "# A test option"
    )
    
    def setup_class(self):
        self.config.add_option(
                option="test",
                type="TestType",
                help="A test option",
                default="default value",
                important_help="The test must pass"
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
                option="test4",
                type="TestType",
                help="A test option",
                important_help="Must be all caps"
                )

    def test_healing(self):
        assert self.config.heal_file(self.broken_config) == self.healed_config 

    def test_type_healing(self):
        assert self.config.heal_file(self.broken_config_with_types, True) == self.healed_config_with_types
