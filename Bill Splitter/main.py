import random


class Party:
    def __init__(self) -> None:
        self.dict_friends = {}
        self.run()

    def run(self):
        number_friends = int(
            input("Enter the name of every friends joining (including you):\n"))
        if number_friends < 1:
            print("No one is joining for the party")
            exit(1)

        print('\nEnter the name of every friend (including you), each on a new line:')
        self.dict_friends = {input(): 0 for _ in range(number_friends)}

        total_bill = float(input("\nEnter the total bill value:\n"))

        lucky_input = input(
            '\nDo you want to use the "Who is lucky?" feature? Write Yes/No:\n')
        if lucky_input == 'Yes':
            lucky_one = Party.choice_lucky(self)
            self.dict_friends = {key: (round(total_bill / (number_friends - 1), 2)
                                       if key != lucky_one else 0) for key in self.dict_friends.keys()}
        elif lucky_input == 'No':
            print("No one is going to be lucky")
            self.dict_friends = {key: round(
                total_bill / number_friends, 2) for key in self.dict_friends.keys()}

        print('\n', self.dict_friends, sep='')

    def choice_lucky(self):
        lucky_one = random.choice(list(self.dict_friends.keys()))
        print(lucky_one, "is the lucky one!")
        return lucky_one


def main():
    _ = Party()


if __name__ == '__main__':
    main()
