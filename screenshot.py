from typing import List
import string
from copy import deepcopy


class ScreenShot(object):
    def __init__(self):
        self.images = {}

    def screen_shot(self, graph: List[List[str]], label: str) -> None:
        """
        capture a screen shot of the graph
        """
        self.images[label] = deepcopy(graph)

    def print_shot(self, label: str):
        """
        Prints sceenshot on the console
        """
        print(label)
        print("_".join(["" for i in range(len(label) + 1)]))
        graph = self.images[label]
        graph_size = len(graph)
        col_name = "    " + " ".join(string.ascii_uppercase[:graph_size])
        print(col_name)
        for i in range(graph_size):
            row = f"{i+1} |" if i + 1 < 10 else f"{i+1}|"
            values = ""
            for j in range(graph_size):
                values += " " + graph[i][j]
            row += values
            print(row)
        print("#".join(["" for i in range(50)]))

    @staticmethod
    def _get_gragh_value(graph: List[List], row: int, col: int) -> str:
        return graph[row][col] if isinstance(graph[row][col], str) else "B"

    def print_two_shot(self, label1: str, label2: str):
        """
        Prints screenshot on the console
        """
        space_len = 20
        space = " ".join(["" for i in range(space_len)])
        print(label1, space, label2)
        print("_".join(["" for i in range(len(label1) + len(label2) + space_len + 2)]))
        graph1 = self.images[label1]
        graph2 = self.images[label2]
        graph_size = len(graph1)
        col_name = "     " + " ".join(string.ascii_uppercase[:graph_size])
        print(col_name, space, col_name)
        for i in range(graph_size):
            row = f"{i+1} |" if i + 1 < 10 else f"{i+1}|"
            values1 = ""
            values2 = ""
            for j in range(graph_size):
                values1 += " " + self._get_gragh_value(graph1, i, j)
                values2 += " " + self._get_gragh_value(graph2, i, j)
            print(row, values1, space, row, values2)
        print("#".join(["" for i in range(len(label1) + len(label2) + space_len + 2)]))

    @property
    def labels(self):
        return self.images.keys()
