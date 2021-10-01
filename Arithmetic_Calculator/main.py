import random

TASK_NUM = 5


def generate_question():
    n1 = random.randint(2, 9)
    n2 = random.randint(2, 9)
    op = random.choice(["+", "-", "*"])
    result = 0
    if op == "+":
        result = n1 + n2
    elif op == "-":
        result = n1 - n2
    elif op == "*":
        result = n1 * n2
    return f"{n1} {op} {n2}", result


def integral_squares():
    number = random.randint(11, 29)
    result = number * number
    return number, result


def intro():
    while True:
        print("Which level do you want? Enter a number:")
        print("1 - simple operations with numbers 2-9")
        print("2 - integral squares of 11-29")
        try:
            option = int(input())
        except ValueError:
            print("Incorrect format.")
            continue
        if option not in [1, 2]:
            print("Incorrect number.")
            continue

        return option


def get_number():
    while True:
        try:
            number = int(input())
        except ValueError:
            print("Wrong format! Try again.")
            continue
        return number


def task(pattern, result, points):
    print(pattern)
    number = get_number()
    if number == result:
        print("Right!")
        points += 1
    else:
        print("Wrong!")
    return points


def main():
    count = 0
    points = 0
    level_desc = ""
    option = intro()
    while TASK_NUM != count:
        if option == 1:
            level_desc = "simple operations with numbers 2-9"
            pattern, result = generate_question()
            points = task(pattern, result, points)
            count += 1

        elif option == 2:
            level_desc = "integral squares of 11-29"
            num, result = integral_squares()
            points = task(num, result, points)
            count += 1

    print(
        f"Your mark is {points}/{TASK_NUM}. Would you like to save the result? Enter yes or no."
    )
    save_op = input().lower()
    if save_op in ["yes", "y"]:
        print("What is your name?")
        name = input()
        with open("results.txt", "a") as file:
            file.write(
                f"{name}: {points}/{TASK_NUM}\n in level {option} ({level_desc})."
            )
            print('The results are saved in "results.txt".')


if __name__ == "__main__":
    main()

