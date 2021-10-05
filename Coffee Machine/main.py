from dataclasses import dataclass

from CoffeeCalculator import CoffeeCalculator


@dataclass
class CoffeeMachine:
    calc_coffee: CoffeeCalculator = CoffeeCalculator()

    def menu(self):

        while True:
            print("\nWrite action (buy, fill, take, remaining, exit):")
            action = input()
            if action not in ["buy", "fill", "take", "remaining", "exit"]:
                print("Wrong action")
                continue
            if action == "buy":
                self.buy()

            elif action == "fill":
                self.fill()

            elif action == "take":
                self.take()

            elif action == "remaining":
                self.print_machine_status(self.calc_coffee)

            elif action == "exit":
                break

    def take(self):
        total_money = self.calc_coffee.take_money()
        print(f"I gave you ${total_money}")

    def fill(self):
        print("Write how many ml of water do you want to add:")
        water = int(input())
        print("Write how many ml of milk do you want to add:")
        milk = int(input())
        print("Write how many grams of coffee beans do you want to add:")
        beans = int(input())
        print("Write how many disposable cups of coffee do you want to add:")
        cups = int(input())
        self.calc_coffee.fill_machine(water, milk, beans, cups)

    def buy(self):
        print(
            "\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:"
        )
        coffee_type = input()
        if coffee_type == "back":
            return
        if coffee_type not in ["1", "2", "3"]:
            print("Wrong coffee type")
            return
        empty_pockets = self.calc_coffee.is_purchasable(coffee_type)
        if len(empty_pockets) == 0:
            print("I have enough resources, making you a coffee!")
            self.calc_coffee.buy_coffee(coffee_type)
        else:
            empty_string = ", ".join(empty_pockets)
            print(f"Sorry, not enough {empty_string}!")

    @staticmethod
    def print_machine_status(machine: CoffeeCalculator):
        print("\nThe coffee machine has:")
        print(f"{machine.c_water} of water")
        print(f"{machine.c_milk} of milk")
        print(f"{machine.c_beans} of coffee beans")
        print(f"{machine.c_cups} of disposable cups")
        print(f"{machine.c_money} of money")


def main():
    coffee_machine = CoffeeMachine()
    coffee_machine.menu()


if __name__ == "__main__":
    main()

