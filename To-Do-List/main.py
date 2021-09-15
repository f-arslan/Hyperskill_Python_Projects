from datetime import date, datetime, timedelta
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import session
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import delete

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.id}. {self.task}"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class Operation:
    def __init__(self):
        pass

    @staticmethod
    def menu():
        while True:
            print("\n1) Today's tasks")
            print("2) Week's tasks")
            print("3) All tasks")
            print("4) Missed tasks")
            print("5) Add task")
            print("6) Delete task")
            print("0) Exit")
            chose = input()
            if chose == "1":
                Operation.today_task()
            elif chose == "2":
                Operation.week_task()
            elif chose == "3":
                Operation.all_task()
            elif chose == "4":
                Operation.miss_task()
            elif chose == "5":
                Operation.add_task()
            elif chose == "6":
                Operation.delete_task()
            if chose == "0":
                break

    @staticmethod
    def delete_task():
        print("Choose the number of the task you want to delete:")
        session = Session() 
        rows = session.query(Table.id, Table.task, Table.deadline).filter(Table.deadline < datetime.today().date()).all()
        if len(rows) == 0:
            print("Nothing to do!\n")
        else:
            for item in rows:
                print(f"{item[0]}. {item[1]}. {item[2].day} {item[2].strftime('%b')}")
        try:
            delete_number = int(input())
        except ValueError:
            print("Enter a integer value.")
        session.query(Table).filter(Table.id == delete_number).delete()
        session.commit()
        print("The task has been deleted!\n")
    
    @staticmethod
    def miss_task():
        print("Missed tasks:")
        session = Session()
        rows = session.query(Table.id, Table.task, Table.deadline).filter(Table.deadline < datetime.today().date()).all()
        if len(rows) == 0:
            print("Nothing is missed!\n")
        else:
            for item in rows:
                print(f"{item[0]}. {item[1]}. {item[2].day} {item[2].strftime('%b')}")
        print()

    @staticmethod
    def week_task():
        today = datetime.today()
        day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        print()
        for _ in range(7):
            print(day_name[today.weekday()], today.day, today.strftime("%b"))
            session = Session()
            rows = session.query(Table).filter(Table.deadline == today.date()).all()
            if len(rows) == 0:
                print("Nothing to do!\n")
            else:
                print(*rows, sep='\n')
                print()
            today = today + timedelta(days=1)

    @staticmethod
    def all_task():
        session = Session()
        print("All tasks:")
        rows = session.query(Table.id, Table.task, Table.deadline).order_by(Table.deadline).all()
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for item in rows:
                print(f"{item[0]}. {item[1]}. {item[2].day} {item[2].strftime('%b')}")

    @staticmethod
    def today_task():
        session = Session()
        today = datetime.today()
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        print(f"\nToday {today.day} {today.strftime('%b')}:")
        if len(rows) > 0:
            print(*rows, sep="\n")
        else:
            print("Nothing to do!")
        session.commit()

    @staticmethod
    def add_task():
        session = Session()
        str_field = input("\nEnter task\n")
        deadline_field = input("Enter deadline\n")
        deadline_field = datetime.strptime(deadline_field, '%Y-%m-%d')
        new_row = Table(task=str_field, deadline=deadline_field)
        print("The task has been added!")
        session.add(new_row)
        session.commit()


Operation.menu()
