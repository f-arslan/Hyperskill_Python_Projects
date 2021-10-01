from dataclasses import dataclass
from collections import defaultdict, OrderedDict
import random


@dataclass
class RandomOperation:
    clear_data: str = ""
    triad_dict = defaultdict(lambda: [0, 0])
    predict: str = ""
    dollar: int = 1000

    def process_data(self, data: str) -> None:
        """Clean data from non-binary characters"""
        for letter in data:
            if letter in ["0", "1"]:
                self.clear_data += letter

    def triad_data(self) -> None:
        """Create a dictionary of triads and their count of 1 and 0"""
        for i in range(len(self.clear_data) - 3):
            if self.clear_data[i + 3] == "1":
                self.triad_dict[self.clear_data[i: i + 3]][1] += 1
            else:
                self.triad_dict[self.clear_data[i: i + 3]][0] += 1

        self.triad_dict = OrderedDict(sorted(self.triad_dict.items()))

    def prediction(self) -> str:
        """It checks the count of 1 and 0 in the triad and returns the most frequent one in the triad"""
        pre_string = "".join(str(random.randint(0, 1)) for _ in range(3))
        for i in range(len(self.clear_data) - 3):
            triad = self.clear_data[i: i + 3]
            if self.triad_dict[triad][1] > self.triad_dict[triad][0]:
                pre_string += "1"
            elif self.triad_dict[triad][1] == self.triad_dict[triad][0]:
                pre_string += random.choice(["0", "1"])
            else:
                pre_string += "0"
        return pre_string

    def compare(self) -> int:
        return sum(self.predict[3:][i] == l for i, l in enumerate(self.clear_data[3:]))

