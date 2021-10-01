from dataclasses import dataclass
from randomOperation import RandomOperation


@dataclass
class RandomNess(RandomOperation):
    limit: int = 100

    def menu(self) -> None:
        self.print_ai()
        while True:
            self.message_info()
            self.process_data(input())
            if len(self.clear_data) >= self.limit:
                self.print_data()
                self.triad_data()
                self.clear_data = ""
                self.second_input()
                break

    def second_input(self) -> None:
        self.print_bet_intro()
        while True:
            print("\nPrint a random string containing 0 or 1:")
            val = input()
            if val == "enough":
                print("Game over!")
                break
            self.process_data(val)
            if len(self.clear_data) == 0:
                continue
            self.triad_data()
            print("prediction:")
            self.predict = self.prediction()
            print(self.predict)
            correct_digit = self.compare()
            false_digit = len(self.clear_data) - correct_digit
            print(
                f"\nComputer guessed right {correct_digit} out of {len(self.clear_data) - 3} symbols ({round(correct_digit/(len(self.clear_data) - 3) * 100, 2)} %)"
            )
            self.dollar = self.dollar - correct_digit + false_digit - 3
            print(f"Your balance is now ${self.dollar}")
            self.clear_data = ""
            self.predict = ""

    def print_data(self) -> None:
        print("\nFinal data string:")
        print(self.clear_data)

    @staticmethod
    def message_intro() -> None:
        print("Print a random string containing 0 or 1:\n")

    def message_info(self):
        print(
            f"Current data length is {len(self.clear_data)}, {self.limit - len(self.clear_data)} symbols left"
        )
        self.message_intro()

    def print_dict(self) -> None:
        for k, v in self.triad_dict.items():
            print(f"{k}: {v[0]},{v[1]}")

    @staticmethod
    def print_ai() -> None:
        print("Please give AI some data to learn...")

    @staticmethod
    def print_bet_intro() -> None:
        print(
            """\nYou have $1000. Every time the system successfully predicts your next press, you lose $1.
Otherwise, you earn $1. Print "enough" to leave the game. Let's go!"""
        )


def main() -> None:
    rand = RandomNess()
    rand.menu()


if __name__ == "__main__":
    main()

