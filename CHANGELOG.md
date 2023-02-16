# Change Log
All notable changes to this project will be documented in this file.

The Major version 1.y.z is to be considered in development; things can break and change at any moment. 
The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## [1.1.1] - 2023-02-16

### Fixed
- Updated GitHub links in the pyproject.toml file.

## [1.1.0] - 2023-02-15

### Added
- Added `get_options` as a getter to allow users to access the list of options of a TypeConfig object.
- Added `get_types` as a getter to allow users to access the list of types of a TypeConfig object.

## [1.0.5] - 2023-02-06

### Fixed
- Moved the type hints parameter from the methods to the class initialisation and changed the healing method's name from `heal_file` to `heal_config`.

## [1.0.4] - 2023-02-04

### Fixed
- Fixed a bug in `validate_config`, which would re-assign the options' value to the whole config (if the value was True, the config would now be "True" instead of {option: True}).

## [1.0.3] - 2023-02-04

### Fixed
- Falsy values are now considered when merging (a `False` will be considered a set value, not something left un-set).
  This was a problem when using `argparse`'s '`action="store_false"`.
  It also implies that when using `store_false` or `store_true` and you don't desire a default False (which could overwrite the config file), you also need to specify `default=None`.

## [1.0.2] - 2023-02-01

### Added
- It's now possible to use multi-line strings for `help` and `important_help` messages.
- Changelog.md has been added to the project.

### Changed
- Changed `add_option`'s `constraints` parameter to `important_help`.
