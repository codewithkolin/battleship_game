import string
import random


def get_cell_name(col: int, row: int) -> str:
    """
    Converts grid postion to board cell address
    """
    colname = string.ascii_uppercase[col]
    return f"{colname}{row+1}"


def create_random_shot(number: int) -> str:
    lst = []
    for i in range(number):
        col = random.choice(string.ascii_uppercase[:10])
        row = random.choice(range(1, 11))
        lst.append(f"{col}{row}")
    return " ".join(lst)
