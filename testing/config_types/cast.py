import config_types.custom_types as ty


def cast_int(number: str) -> int:
    return int(number)

def cast_myType(something: str) -> ty.MyType:
    return something

def cast_myList(something: str) -> ty.MyList:
    myList = something.split(",")
    cleaned_list = [x.strip() for x in myList]
    return cleaned_list

def cast_ExistingPath(path: str) -> ty.ExistingPath:
    return path
