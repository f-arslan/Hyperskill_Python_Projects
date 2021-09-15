import random
from collections import defaultdict
global options
options = ["rock", "fire", "scissors", "snake", "human", "tree", "wolf", "sponge", "paper", "air", "water", "dragon", "devil", "lightning", "gun"]
counter_dict = {
    "rock": (1, 7), "fire": (2, 8), "scissors": (3, 9), "snake": (4, 10), "human": (5, 11), "tree": (6, 12),
    "wolf": (7, 13), "sponge": (8, 14), "paper": (9, 14, 0, 0), "air": (10, 14, 0, 1), "water": (11, 14, 0, 2),
    "dragon": (0, 3, 12, 14), "devil": (0, 4, 13, 14), "lightning": (0, 5, 14, 14), "gun": (0, 6)
}

global scores
scores = {}
user_options = {}


def menu():
    user_name = input("Enter your name: ")
    print(f"Hello, {user_name}")
    rating()
    option_user = input().split(",")
    if option_user == ['']:
        user_options[user_name] = ["rock", "paper", "scissors"]
    else:
        user_options[user_name] = option_user
    if user_name not in scores.keys():
        scores[user_name] = 0
    print("Okay, let's start")
    while True:
        user_input = input()
        if user_input == "!exit":
            print("Bye!")
            break
        if user_input == "!rating":
            show_rating(user_name)
            continue
        if user_input not in counter_dict.keys():
            print("Invalid input")
            continue
        computer_choice = random.choice(user_options[user_name])
        if user_name not in scores.keys():
            scores[user_name] = 0
        beat_range = counter_dict[user_input]
        if computer_choice in options[beat_range[0]:beat_range[1] + 1] and user_input in user_options[user_name]:
            print("Well done. The computer chose " + computer_choice + " and failed")
            scores[user_name] += 100
            continue

        if len(beat_range) > 2:
            if computer_choice in options[beat_range[2]: beat_range[3] + 1] and user_input in user_options[user_name]:
                print("Well done. The computer chose " + computer_choice + " and failed")
                scores[user_name] += 100

        if computer_choice == user_input:
            print(f"There is a draw ({user_input})")
            scores[user_name] += 50
        else:
            print(f"Sorry, but the computer chose {computer_choice}")


def show_rating(user_name: str):
    if user_name in scores.keys():
        print(f"Your rating: {scores[user_name]}")
    else:
        print(f"Your rating: 0")


def rating():
    with open("rating.txt", "r") as f:
        result = [x.strip() for x in f.readlines()]
        for items in result:
            item = items.split()
            scores[item[0]] = int(item[1])


def main():
    menu()


if __name__ == "__main__":
    main()
