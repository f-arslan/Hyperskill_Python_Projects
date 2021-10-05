from dataclasses import dataclass


@dataclass
class CoffeeCalculator:
    ESPRESSO_WATER: int = 250
    ESPRESSO_MILK: int = 75
    ESPRESSO_BEANS: int = 16
    ESPRESSO_COST: int = 4

    LATTE_WATER: int = 350
    LATTE_MILK: int = 75
    LATTE_BEANS: int = 20
    LATTE_COST: int = 7

    CAPPUCCINO_WATER: int = 200
    CAPPUCCINO_MILK: int = 100
    CAPPUCCINO_BEANS: int = 12
    CAPPUCCINO_COST: int = 6

    c_cups: int = 9
    c_water: int = 400
    c_milk: int = 540
    c_beans: int = 120
    c_money: int = 550
    ingredient = {}

    def buy_coffee(self, coffee_type) -> None:
        if coffee_type == "1":
            self.c_water -= self.ESPRESSO_WATER
            self.c_beans -= self.ESPRESSO_BEANS
            self.c_money += self.ESPRESSO_COST
            self.c_cups -= 1

        elif coffee_type == "2":
            self.c_water -= self.LATTE_WATER
            self.c_milk -= self.LATTE_MILK
            self.c_beans -= self.LATTE_BEANS
            self.c_money += self.LATTE_COST
            self.c_cups -= 1

        elif coffee_type == "3":
            self.c_water -= self.CAPPUCCINO_WATER
            self.c_milk -= self.CAPPUCCINO_MILK
            self.c_beans -= self.CAPPUCCINO_BEANS
            self.c_money += self.CAPPUCCINO_COST
            self.c_cups -= 1

    def fill_machine(self, water, milk, beans, cups) -> None:
        self.c_water += water
        self.c_milk += milk
        self.c_beans += beans
        self.c_cups += cups

    def take_money(self) -> int:
        money = self.c_money
        self.c_money = 0
        return money

    def is_purchasable(self, coffee_type) -> list:
        empty_pockets = []
        if coffee_type == "1":
            if self.c_water <= self.ESPRESSO_WATER:
                empty_pockets.append("water")
            if self.c_beans <= self.ESPRESSO_BEANS:
                empty_pockets.append("beans")
            if self.c_cups <= 0:
                empty_pockets.append("cups")

        elif coffee_type == "2":
            if self.c_water <= self.LATTE_WATER:
                empty_pockets.append("water")
            if self.c_milk <= self.LATTE_MILK:
                empty_pockets.append("milk")
            if self.c_beans <= self.LATTE_BEANS:
                empty_pockets.append("beans")
            if self.c_cups <= 0:
                empty_pockets.append("cups")

        elif coffee_type == "3":
            if self.c_water <= self.CAPPUCCINO_WATER:
                empty_pockets.append("water")
            if self.c_milk <= self.CAPPUCCINO_MILK:
                empty_pockets.append("milk")
            if self.c_beans <= self.CAPPUCCINO_BEANS:
                empty_pockets.append("beans")
            if self.c_cups <= 0:
                empty_pockets.append("cups")

        return empty_pockets

