from type_config import TypeConfig

class TypeConfig:
    clean_file = TypeConfig()._clean_file

    formatted_config="""
    option = value
    # !!! something
    # another comment

    another_option = value
    # another comment
    """
    cleaned_config = "option = value\nanother_option = value"

    formatted_config_with_types="""
    [some type] option = value
    # !!! something
    # another comment

    [AnotherType] another_option = value
    # another comment
    """
    cleaned_config_with_types = "[some type] option = value\n[AnotherType] another_option = value"


    def test_cleaning_without_type(self):
        assert self.clean_file(self.formatted_config) == self.cleaned_config 

    def test_cleaning_with_type(self):
        assert self.clean_file(self.formatted_config_with_types) == self.cleaned_config_with_types



