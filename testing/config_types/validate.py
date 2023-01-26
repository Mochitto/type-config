import string
import os

def validate_int(number: str) -> bool:
    try:
        return int(number) <= 100
    except ValueError:
        return False

def validate_MyType(something: str) -> bool:
    for char in something:
        if char not in string.ascii_letters:
            return False
    return True

def validate_MyList(list_of_things: str) -> bool:
    things = list_of_things.split(",")
    return len(things) == 3

def validate_ExistingPath(path: str) -> bool:
    try:
        is_abs = os.path.isabs(path)
        does_exists = os.path.exists(path)
    except:
        return False
    return is_abs and does_exists
