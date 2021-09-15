from collections import defaultdict
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MyClass(Base):
    __tablename__ = "flashcard"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box_number = Column(Integer)


engine = create_engine("sqlite:///flashcard.db?check_same_thread=False")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Flashcards:
    def __init__(self):
        self.flashcards = defaultdict(str)

    def menu(self):
        while True:
            print("1. Add flashcards")
            print("2. Practice flashcards")
            print("3. Exit")
            chc = input()
            if chc not in ["1", "2", "3"]:
                print(f"\n{chc} is not an option\n")
                continue
            chc = int(chc)
            print()
            if chc == 1:
                Flashcards.add_flashcards(self)
            elif chc == 2:
                Flashcards.practice_flashcards()
            elif chc == 3:
                print("Bye!\n")
                break

    def add_flashcards(self):
        while True:
            print("1. Add a new flashcard")
            print("2. Exit")
            chc = input()
            if chc not in ["1", "2"]:
                print(f"\n{chc} is not an option\n")
                continue
            chc = int(chc)
            print()
            if chc == 1:
                Flashcards.add_new_flashcards(self)
            elif chc == 2:
                break

    def add_new_flashcards(self):
        while True:
            print("Question:")
            quest = input()
            if len(quest) > 2:
                break
        while True:
            print("Answer:")
            answer = input()
            if len(answer) > 2:
                break
        self.flashcards[quest] = answer
        new_card = MyClass(question=quest, answer=answer, box_number=1)
        session.add(new_card)
        session.commit()
        print()

    @staticmethod
    def practice_flashcards():
        all_cards = session.query(MyClass).all()

        if len(all_cards) == 0:
            print("There is no flashcard to practice!\n")
        else:
            for quest in all_cards:
                print(f"\nQuestion: {quest.question}")
                while True:
                    print('press "y" to see the answer:')
                    print('press "n" to skip:\npress "u" to update:')
                    chc = input()
                    if chc not in ["u", "y", "n"]:
                        print(f"{chc} not in option")
                    if chc == "y":
                        print(f"\nAnswer: {quest.answer}\n")
                        Flashcards.box_update(quest.question)
                        break
                    elif chc == "u":
                        Flashcards.update_card(quest.question)
                        break
                    elif chc == "n":
                        Flashcards.box_update(quest.question)
                        break

    @staticmethod
    def box_update(update_quest):
        while True:
            entries = session.query(MyClass).all()
            print(
                'press "y" if your answer is correct:\npress "n" if your answer is wrong:'
            )
            chc = input()
            if chc not in ["y", "n"]:
                continue
            if chc == "y":
                for entry in entries:
                    if entry.question == update_quest:
                        entry.box_number += 1
                        session.commit()
                        if (
                            entry.box_number == 4
                        ):  # If the number reach 4 in database then delete the entry.
                            session.delete(entry)
                            session.commit()
                        break
                break
            elif chc == "n":
                for entry in entries:
                    if entry.question == update_quest:
                        if entry.box_number == 1:
                            break
                        entry.box_number -= 1
                        session.commit()
                        break
                break
            else:
                print(f"\n{chc} is not an option\n")
            break

    @staticmethod
    def update_card(update_question):
        while True:
            print(
                'press "d" to delete the flashcard:\npress "e" to edit the flashcard:'
            )
            entries = session.query(MyClass).all()
            opt = input()
            if opt not in ["d", "e"]:
                print(f"{opt} is not an option")
                continue
            if opt == "e":
                for entry in entries:
                    if entry.question == update_question:
                        print(f"\ncurrent question: {update_question}")
                        print("please write a new question: ")
                        new_quest = input()
                        while True:
                            if len(new_quest) > 5:
                                entry.question = new_quest
                                session.commit()
                                break
                        print(f"\ncurrent answer: {entry.answer}")
                        print("please write a new answer:")
                        new_answer = input()
                        while True:
                            if len(new_answer) > 2:
                                entry.answer = new_answer
                                session.commit()
                                break
                break
            if opt == "d":
                for entry in entries:
                    if entry.question == update_question:
                        session.delete(entry)
                        session.commit()
                        break
                break


flashcards = Flashcards()
flashcards.menu()
