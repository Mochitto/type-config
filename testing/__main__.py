from easy_config import EasyConfig

from config_types.cast import *
from config_types.validate import *

my_config = EasyConfig("./config.mochi")

my_config.add_type("int", validate_int, cast_int, "Must be an integer number and less than 100.")
my_config.add_type("MyType", validate_MyType, cast_myType, "Must only contain letters from the English alphabet.")
my_config.add_type("MyList", validate_MyList, cast_myList, "Must have 3 entries, separated by commas.")
my_config.add_type("ExistingPath", validate_ExistingPath, cast_ExistingPath, "Must be an absolute path to an existing directory.")

my_config.add_option(
        type="int", 
        option="Money", 
        default="50",
        optional=True,
        help="The amount of money you can use in the shop."
        )
my_config.add_option(
        type="MyType", 
        option="Shop's name",
        default="something",
        constraints="Can only be letters from the English alphabet (a to z)",
        help="Where you are going to shop."
        )
my_config.add_option(
        type="MyList", 
        option="What to buy",
        optional=True,
        constraints="Must be three objects, divided by commas",
        help="What you are going to buy."
        )
my_config.add_option(
        type="ExistingPath", 
        option="Out directory",
        default="/Path/to/your/folder",
        constraints="Must be an absolute path to an existing folder",
        help="Where your shopping list will be sent."
        )

# my_config.write_config()
# parsed_config, errors = my_config.parse_file()

# print(parsed_config)
# if errors:
#     print("❌ There was something wrong with the configurations:")
# for error in errors:
#     print("--- " + error)

# print(my_config.validate_config({
#     "Money": "102",
#     "Shop's name": "awala",
#     "What to buy": None
#     }))

my_config.heal_file()
