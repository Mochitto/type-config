# Type config ⭐🐙

`Type-config` is a small python library that let's you add custom types and validations to your config file.
The project's focus is on readability and maintainability, using a simple ini-like formatting.

This project is being tested and very young. There could be updates soon and not everything might work as expected.<br>
If you find a problem, please write an issue, so I'll be able to solve it :)

## Table of contents (for github) 📝
- [Type config ⭐🐙](#type-config-)
  - [Features](#features)
  - [Demo](#demo)
- [Getting started](#getting-started)
  - [Installation 🔧](#installation-)
  - [Adding options](#adding-options)
  - [Adding types](#adding-types)
  - [Creating a file](#creating-a-file)
  - [Parsing a file](#parsing-a-file)
  - [Validating an existing dictionary](#validating-an-existing-dictionary)
  - [Merging configurations](#merging-configurations)
  - [Healing a broken configuration](#healing-a-broken-configuration)
  - [Error handling 🔧](#error-handling-)
- [Contributing 💕](#contributing-)
- [Extra 🐙](#extra-)

## Features
- Define custom types for the validation of your config file's data, applied during parsing
- Automatic formatting of your config file
- Possibility of recovering a corrupted (badly formatted) file
- Merging configurations (useful when having CLI arguments and a config file)
- Attaching error and help messages to each option, for clear and effective communication 

## Demo
This is how you would create a `type_config` object:
```python
config = TypeConfig()
```
Adding options:
```python
config.add_option(
  option="shopping list",
  type="List>=3",
  help="What I have to buy",
  important_help="Must be a list of at least three items, separated by commas",
)
```
Adding a type (they can have descriptive names❗):
```python
config.add_type(
  type="List>=3",
  validate=lambda list: len(list.split(",")) >= 3,
  cast=lambda list: [item.trim() for item in list.split(",")],
  error="The list must have at least three items"
)
```
This is how entries can look in a config file made with `type_config`:
```ini
shopping list = water, pasta, oil
# !!! Must be a list of at least three items, separated by commas
# What I have to buy
```
or, if you want to see what type you are applying to the option:
```ini
[List>=3] shopping list = water, pasta, oil
# !!! Must be a list of at least three items, separated by commas
# What I have to buy
```
When you parse this file again, each option will be tested with their type's validating function and formatted using their casting function.

If there are errors, the parsing won't crash; it will give you a list of which options failed and why, so that you can quickly understand what's wrong.

---
# Getting started 🔥
## Installation 🔧
Install the package using pip
```bash
pip install type_config
```

## Adding options
Options are added using the method `add_option` of a TypeConfig object.

They hold many information useful when parsing and debugging.
 Parmeter | Description | Default 
 :---- | :---- | :---- 
 `option` | The option's name | `Required` 
 `type` | The type associated with this option | `Required`
 `help` | An help string used to explain what the option does or what it is for.<br>This is showed under the option in the config file. | `Required`
 `default` | A default value used when the option is left blank | `Empty_string`
 `can_be_empty` | Whether or not the option can be left without a value.<br>The value that will be given is `None`.<br>Notice: default is applied when there is no value, so it's suggested using this option while leaving `default` empty. | `False`
 `important_help` | Extra information that could be useful when writing the option's value | `Empty_string`

## Adding types
Types are added using the method `add_type` of a TypeConfig object.

They are used for data validation.
 Parmeter | Description | Default 
 :---- | :---- | :---- 
 `type` | The type's name | `Required`
 `validate` | A function that returns a boolean, which is used to validate the option's value. | `Required`
 `cast` | A function that "casts" a specific type upon the option's value, effectively transforming it from string to the desired type. | `Required`
 `error` | A message describing what could be the reason when the option's value is considered invalid.<br>This is showed under the option in the config file. | `Required`

## Creating a file
You can obtain the formatted text of a config file with the `create_config` method of a TypeConfig's object.

Notice: the library doesn't write directly to a file, instead it returns a string that can be written to an ini file.
This is done so that the user has more control over the output path and exceptions handling.

 Parmeter | Description | Default 
 :---- | :---- | :---- 
 `format_with_types` | Whether or not to include type hints in the config file. These are mainly for development.<br>Type hints do not change the parsing steps and can be added or removed at any time, using the `heal_config` method. | `False`

## Parsing a file
You can obtain a dictionary with your validated data using the `parse_config` method of a TypeConfig object.

This method returns a tuple of two values, containing the configuration data, represented as {option:value}, and a dictionary with errors that happened during parsing, represented as {option: error}.

Notice: the library doesn't read directly from a file, instead it reads a string.
This is done so that the user has more control over the input path and exceptions handling.

 Parmeter | Description | Default 
 :---- | :---- | :---- 
 `file_content` | A string representing the config file to be parsed. | `Required`
 
 ## Validating an existing dictionary
 You might want to validate an existing dictionary (for example, when working with both arguments from a CLI and a config file).
 This can be done by using the `validate_config` method of a TypeConfig object.

 This method works in a similar way as `parse_config`, but takes a dictionary instead of a string. It also returns both a dictionary with the validated data and a dictionary with errors that happened during validation.

 Parmeter | Description | Default 
 :---- | :---- | :---- 
 `config` | A dictionary containing keys that are part of the TypeConfig's options. | `Required`

## Merging configurations
To merge two configurations, you can use the `merge_config` method of a TypeConfig object.<br>
This method creates a new dictionary containing {option:value}. 

The options' values priority is: 
1. Overwriting_config's value 
2. Overwritable_config's value
3. Default value from the TypeConfig object 
4. raise `ParsingError` if option can't be empty, else value is `None`

Notice: no validation is done during this operation and only options present in the input configurations will be written to the result.

 Parmeter | Description | Default 
 :---- | :---- | :---- 
 `Overwriting_config` | The configuration dictionary which values will be preferred when merging. | `Required`
 `Overwritable_config` | The configuration dictionary which values will be overwritten, if possible. | `Required`

## Healing a broken configuration
The library has a method for "healing" badly formatted configurations, which is the `heal_config` method of a TypeConfig object. This method maintains {option: value} pairs if the option, equal sign and value are formatted correctly and the option is part of the TypeConfig object. This method also restores comments and whitespaces.

The returning value is a string (the healed configuration).

Example:
```ini
BrokenType] with a broken option #Added an inline comment

I'm an option that dones't exist = ahah

option = my value # another inline comment
# I changed the help line
```
will become:
```ini
[BrokenType] with a broken option = default
# !!! This are the important_help
# And this is the help line

[BrokenType] option = my value
# !!! This are the important_help
# And this is the original help line
```

 Parmeter | Description | Default 
 :---- | :---- | :---- 
 `file_content` | A string representing the broken file content to restore. | `Required`
 `format_with_types` | Whether or not to include type hints in the restored config file. These are mainly for development.<br>Type hints do not change the parsing steps and can be added or removed safely at any time using this method. | `False`

 ## Error Handling 🔧
This library has only two kinds of errors: `ParsingError` and `ValidationError`.<br>They can be imported using:
```python
from type_config.errors import ParsingError, ValidationError
```
This is a list of when they are used (all of these errors should be handled internally):

 Error | Situations | Methods 
 :---- | :---- | :----- 
 `ParsingError` |- When an option  isn't part of the TypeConfig's object configuration<br>- When an option that can't be left empty is None/Falsy<br> | `parse_config`
 `ValidationError` | -  When a type or an option isn't part of the TypeConfig's object configuration<br>- When an option that can't be left empty is None/Falsy<br>- When a value is invalid (Custom error message) | `prase_config`, `validate_config`

# Contributing 💕
Feel free to open issues asking for more information or to reach out to me!

- Please make sure all the [tests](https://github.com/Mochitto/type_config/tree/main/tests) are passing before opening a pull request. You can use [pytest](https://pypi.org/project/pytest/) for this.
- Please use types when possible (you can be helped by [pyright](https://pypi.org/project/pyright/) or [mypy](https://pypi.org/project/mypy/)).
- Please don't reformat the file in the same commit as your refactoring/contribution (if you want to, use [black](https://pypi.org/project/black/)); this is best done in its own commit, to make clear what changed in which commit.
- Please do not use abbreviations when naming variables or functions (I have an hard time understanding them :( ).
- Please append `Feat`, `Refactor`, `Fix`, `Format` to make clear what you've contributed on.

# Extra 🐙
Built with love at [Recurse Center](https://www.recurse.com/)

![Recurse center's logo](https://d29xw0ra2h4o4u.cloudfront.net/assets/logo_square-60e12570c3a1b0b0798e651a0755f71a40ff15421761b786f720e4c02fc89a1f.png)
