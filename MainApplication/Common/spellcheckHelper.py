import re

scH_special_characters = re.compile(r'[@!#$%^&*()<>?/\|}{~:]')


def contains_special_characters(string: str) -> bool:
    if scH_special_characters.search(string) is None:
        return False
    return True
