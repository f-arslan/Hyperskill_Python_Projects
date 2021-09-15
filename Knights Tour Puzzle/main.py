global moves
moves = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]


class Board:
    def __init__(self) -> None:
        self.board = []
        self.knight_x = 0
        self.knight_y = 0
        self.board_x = 0
        self.board_y = 0
        self.star_places = []
        self.coords = []
        self.blank_size = 0
        self.run()

    def run(self):
        while True:
            board_dimension = input("Enter your board dimensions: ").split()
            if (
                all([x.isdigit() for x in board_dimension])
                and len(board_dimension) == 2
                and (all([int(x) > 0 for x in board_dimension]))
            ):
                start_pos = input("Enter the knight's starting position: ").split()
                if all([x.isdigit() for x in start_pos]) and (len(start_pos) == 2):
                    between_condition = (
                        1 <= int(start_pos[1]) <= int(board_dimension[1])
                    ) and (1 <= int(start_pos[0]) <= int(board_dimension[0]))
                    if between_condition:
                        total_size = int(board_dimension[0]) * int(board_dimension[1])
                        blank_size = Board.find_digits(total_size)
                        self.board = [
                            ["_" * blank_size for _ in range(int(board_dimension[0]))]
                            for _ in range(int(board_dimension[1]))
                        ]
                        self.board_x = int(board_dimension[1])
                        self.board_y = int(board_dimension[0])
                        self.knight_x = int(start_pos[1]) - 1
                        self.knight_y = int(start_pos[0]) - 1
                        self.blank_size = blank_size
                        Board.do_choice(
                            self,
                            int(board_dimension[0]),
                            int(board_dimension[1]),
                            blank_size,
                        )
                        self.board = [
                            ["_" * blank_size for _ in range(int(board_dimension[0]))]
                            for _ in range(int(board_dimension[1]))
                        ]
                        self.board[self.knight_x][self.knight_y] = (
                            " " * (blank_size - 1) + "X"
                        )
                        Board.scenario(self, blank_size)
                        break
                    else:
                        print("Invalid position!")
                else:
                    print("Invalid position!")
            else:
                print("Invalid dimensions!")

    def scenario(self, blank_size):
        coords = Board.move_knight(self, self.knight_x, self.knight_y, blank_size)
        Board.draw_board(self, blank_size)
        Board.next_move(self, coords, blank_size)

    def do_choice(self, board_x, board_y, blank_size):
        while True:
            choice = input("Do you want to try the puzzle? (y/n): ").split()
            code = 0
            if len(choice) == 1:
                chc = choice[0].lower()
                if chc.isalpha():
                    if chc == "y":
                        code = 1
                        Board.backtrack(self, blank_size, code)
                        break
                    elif chc == "n":
                        code = 2
                        Board.backtrack(self, blank_size, code)
                        exit()
                    else:
                        print("Wrong input")
            else:
                print("Wrong input")

    def backtrack(self, blank_size, code):
        self.board[self.knight_x][self.knight_y] = " " * (blank_size - 1) + str(1)
        counter = 2
        x = self.knight_x
        y = self.knight_y
        status = 0
        for i in range(self.board_x * self.board_y - 1):
            digits = Board.find_digits(counter)
            pos = Board.get_possibilities(self, x, y)
            if len(pos) == 0:
                print("No solution exists!")
                status = 1
                break
            minimum = pos[0]
            for p in pos:
                if len(Board.get_possibilities(self, p[0], p[1])) <= len(
                    Board.get_possibilities(self, minimum[0], minimum[1])
                ):
                    minimum = p
            x = minimum[0]
            y = minimum[1]
            self.board[x][y] = " " * (blank_size - digits) + str(counter)

            counter += 1
        if code == 1 and status == 1:
            exit()
        elif code == 2 and status != 1:
            Board.draw_board(self, blank_size)

    def get_possibilities(self, x, y):
        pos_x = (2, 1, 2, 1, -2, -1, -2, -1)
        pos_y = (1, 2, -1, -2, 1, 2, -1, -2)
        possibilities = []
        for i in range(8):
            if (
                x + pos_x[i] >= 0
                and x + pos_x[i] <= self.board_x - 1
                and y + pos_y[i] >= 0
                and y + pos_y[i] <= self.board_y - 1
                and self.board[x + pos_x[i]][y + pos_y[i]] == "_" * self.blank_size
            ):
                possibilities.append([x + pos_x[i], y + pos_y[i]])
        return possibilities

    def move_knight(self, knight_x, knight_y, blank_size):
        """Check 8 moves"""
        board = self.board
        coords = []
        for move in moves:
            star_con = [knight_x + move[0], knight_y + move[1]] in self.star_places
            if (
                (0 <= knight_x + move[0] <= self.board_x - 1)
                and (0 <= knight_y + move[1] <= self.board_y - 1)
                and (star_con is False)
            ):
                board[knight_x + move[0]][knight_y + move[1]] = " " * (
                    blank_size - 1
                ) + str(
                    Board.possible_moves(self, knight_x + move[0], knight_y + move[1])
                )
                coords.append([knight_x + move[0], knight_y + move[1]])

        return coords

    def possible_moves(self, knight_x, knight_y):
        c = 0
        for move in moves:
            con = (knight_x + move[0] == self.knight_x) and (
                knight_y + move[1] == self.knight_y
            )
            star_con = [knight_x + move[0], knight_y + move[1]] in self.star_places
            if (
                (0 <= knight_x + move[0] <= self.board_x - 1)
                and (0 <= knight_y + move[1] <= self.board_y - 1)
                and (con is False)
                and (star_con is False)
            ):
                c += 1
        return c

    def next_move(self, coords: list, blank_size):
        a = 0
        while True:
            if a == 0:
                coord = [int(x) for x in input("Enter your next move: ").split()]
                coord_x = coord[1] - 1
                coord_y = coord[0] - 1
                base_con = (coord_x == self.knight_x) and (coord_y == self.knight_y)
                if [coord_x, coord_y] in coords and base_con is False:
                    self.board[self.knight_x][self.knight_y] = (
                        " " * (blank_size - 1) + "*"
                    )
                    self.knight_x = coord_x
                    self.knight_y = coord_y
                    self.board[self.knight_x][self.knight_y] = (
                        " " * (blank_size - 1) + "X"
                    )

                    coords = Board.clean_others(self, blank_size)
                    Board.draw_board(self, blank_size)
                    if len(coords) == 0:
                        a = 1
                        continue

                else:
                    print("Invalid move!", end=" ")
            else:
                if len(self.star_places) + 1 == len(
                    [x for row in self.board for x in row]
                ):
                    print("What a great tour! Congratulations!")
                    break
                else:
                    print("No more possible moves!")
                    print(f"Your knight visited {len(self.star_places) + 1} squares!")
                    break

    def clean_others(self, blank_size):
        board = self.board
        for idx, row in enumerate(board):
            for idy, blank in enumerate(row):
                for char in blank:
                    if char.isdigit():
                        self.board[idx][idy] = "_" * blank_size
                if "*" in blank and [idx, idy] not in self.star_places:
                    self.star_places.append([idx, idy])

        coords = Board.move_knight(self, self.knight_x, self.knight_y, blank_size)
        return coords

    def draw_board(self, blank_size):
        stack = []
        c = 0
        for i in reversed(range(len(self.board))):
            len_number = Board.find_digits(i + 1)
            if len_number == 2:
                a = str(i + 1) + "| " + " ".join(self.board[i]) + " |"
                c = 1
            elif len_number != 2 and c == 1:
                a = " " + str(i + 1) + "| " + " ".join(self.board[i]) + " |"
            else:
                a = str(i + 1) + "| " + " ".join(self.board[i]) + " |"
            b = "| " + " ".join(self.board[i]) + " |"
            if i == self.board_x - 1 and c == 1:
                print(" " * len_number + "-" * len(b))
            elif i == self.board_x - 1 and c == 0:
                print(" " * len_number + "-" * len(b))
            print(a)
            if i == 0 and c == 1:
                print(" " + " " * len_number + "-" * len(b))
            elif i == 0 and c != 1:
                print(" " * len_number + "-" * len(b))
        for j in range(1, self.board_y + 1):
            len_j = Board.find_digits(j)
            stack.append(" " * (blank_size - len_j + 1) + str(j))
        if self.board_y == 1:
            print("  " * blank_size + "".join(stack))
        else:
            print(" " * blank_size + "".join(stack))
        print()

    @staticmethod
    def find_digits(number):
        count = 0
        while number > 0:
            number = number // 10
            count = count + 1

        return count


def main():
    _ = Board()


if __name__ == "__main__":
    main()
