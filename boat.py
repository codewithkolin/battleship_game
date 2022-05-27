from typing import Tuple


class Boat(object):
    """
    Boat class
    """

    def __init__(
        self,
        label: str,
        size: int,
        start_position: Tuple[int, int] = None,
        end_position: Tuple[int, int] = None,
        orientation: str = "v",
    ):
        self.label: str = label
        self.size: int = size
        self.start_position: Tuple[int, int] = start_position
        self.end_position: Tuple[int, int] = end_position
        if self.size == 1 and not end_position:
            self.end_position = start_position
        self.orientation: str = orientation

    def __repr__(self):
        return self.label.capitalize()

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.label == other.label
            and self.size == other.size
            and self.start_position == other.start_position
            and self.end_position == other.end_position
            and self.orientation == other.orientation
        )
