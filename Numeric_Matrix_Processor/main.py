from math import floor, ceil


class Matrix:
    def __init__(self) -> None:
        self.row = []
        self.col = []
        self.matrix = []
        self.rows = []
        self.cols = []

    def run_total(self):
        i = 0
        while i < 2:
            if i == 0:
                row_col = [int(x) for x in input("Enter size of first matrix: ").split()]
                print("Enter first matrix:")
            else:
                row_col = [int(x) for x in input("Enter size of second matrix: ").split()]
                print("Enter second matrix:")
            matrix = [[float(x) for x in input().split()] for _ in range(row_col[0])]
            self.matrix.append(matrix)
            self.row.append(row_col[0])
            self.col.append(row_col[1])
            i += 1

        row_check = [x for x in self.row]
        col_check = [x for x in self.col]
        total_matrix = []
        if row_check[0] == row_check[1] and col_check[0] == col_check[1]:
            total_matrix = Matrix.sum_matrix(self)
        else:
            print('ERROR')
            exit(1)

        Matrix.print_matrix(total_matrix)
        self.matrix = []
        self.row = []
        self.col = []

    def sum_matrix(self):
        new_matrix = [[0 for _ in range(self.col[0])] for _ in range(self.row[0])]

        for i in range(self.row[0]):
            for j in range(self.col[0]):
                new_matrix[i][j] = self.matrix[0][i][j] + self.matrix[1][i][j]

        return new_matrix

    @staticmethod
    def print_matrix(total_matrix):
        print("The result is:")
        for i in range(len(total_matrix)):
            for j in range(len(total_matrix[0])):
                print((floor(total_matrix[i][j] * 100) / 100.0), end=" ")
            print()
        print()

    @staticmethod
    def run_multiply_number():
        try:
            row_col = [int(x) for x in input("Enter size of matrix: ").split()]
            print("Enter matrix:")
            matrix = [[float(x) for x in input().split()] for _ in range(row_col[0])]
            product_with = float(input("Enter constant: "))
            Matrix.multiply_with(matrix, product_with, row_col[0], row_col[1])
        except ValueError:
            print("ERROR")

    @staticmethod
    def multiply_with(matrix, value, row, col):
        new_matrix = [[0 for _ in range(col)] for _ in range(row)]
        for i in range(row):
            for j in range(col):
                new_matrix[i][j] = value * matrix[i][j]

        Matrix.print_matrix(new_matrix)

    def run_multiply_matrix(self):
        self.row = []
        self.col = []
        self.matrix = []
        i = 0
        while i < 2:
            if i == 0:
                row_col = [int(x) for x in input("Enter size of first matrix: ").split()]
                print("Enter first matrix:")
            else:
                row_col = [int(x) for x in input("Enter size of second matrix: ").split()]
                print("Enter second matrix:")
            matrix = [[float(x) for x in input().split()] for _ in range(row_col[0])]
            self.matrix.append(matrix)
            self.row.append(row_col[0])
            self.col.append(row_col[1])
            i += 1

        row_check = [x for x in self.row]
        col_check = [x for x in self.col]
        if row_check[1] == col_check[0]:
            Matrix.multiply_matrix(self, row_check[0], col_check[1])
        else:
            print("The operation cannot be performed.")

    def multiply_matrix(self, row, col):
        mul_matrix = [[0 for _ in range(col)] for _ in range(row)]
        for i in range(len(self.matrix[0])):
            for j in range(len(self.matrix[1][0])):
                for k in range(len(self.matrix[1])):
                    mul_matrix[i][j] += self.matrix[0][i][k] * self.matrix[1][k][j]

        Matrix.print_matrix(mul_matrix)

    @staticmethod
    def run_transpose():
        print("1. Main diagonal")
        print("2. Side diagonal")
        print("3. Vertical line")
        print("4. Horizontal line")
        chc = int(input("Your choice: "))
        if chc == 1:
            Matrix.main_diagonal()
        if chc == 2:
            Matrix.side_diagonal()
            pass
        if chc == 3:
            Matrix.vertical_line()
            pass
        if chc == 4:
            Matrix.horizontal_line()
            pass

    @staticmethod
    def horizontal_line():
        row_col = [int(x) for x in input("Enter matrix size: ").split()]
        print("Enter matrix:")
        matrix = [[float(x) for x in input().split()] for _ in range(row_col[0])]
        Matrix.print_matrix(list(reversed(matrix)))

    @staticmethod
    def vertical_line():
        row_col = [int(x) for x in input("Enter matrix size: ").split()]
        print("Enter matrix:")
        matrix = [[float(x) for x in input().split()] for _ in range(row_col[0])]
        new_matrix = [[0 for _ in range(row_col[0])] for _ in range(row_col[1])]
        for i in range(len(new_matrix)):
            matrix[i].reverse()
            new_matrix[i] = matrix[i]

        Matrix.print_matrix(new_matrix)

    @staticmethod
    def side_diagonal():
        row_col = [int(x) for x in input("Enter matrix size: ").split()]
        print("Enter matrix:")
        matrix = [[float(x) for x in input().split()] for _ in range(row_col[0])]
        new_matrix = [[0 for _ in range(row_col[0])] for _ in range(row_col[1])]

        for i in range(len(new_matrix)):
            for j in range(len(new_matrix[0])):
                for k in range(len(new_matrix)):
                    for t in range(len(new_matrix[0])):
                        if (t + i) == len(new_matrix) - 1 and (k + j) == len(new_matrix) - 1:
                            new_matrix[i][j] = matrix[k][t]
                            break
                    if new_matrix[i][j] != 0:
                        break

        Matrix.print_matrix(new_matrix)

    @staticmethod
    def main_diagonal():
        row_col = [int(x) for x in input("Enter matrix size: ").split()]
        print("Enter matrix:")
        matrix = [[float(x) for x in input().split()] for _ in range(row_col[0])]
        new_matrix = [[0 for _ in range(row_col[0])] for _ in range(row_col[1])]

        for i in range(len(new_matrix)):
            for j in range(len(new_matrix[0])):
                new_matrix[i][j] = matrix[j][i]

        Matrix.print_matrix(new_matrix)

    @staticmethod
    def menu_determinant():
        row_col = [int(x) for x in input("Enter matrix size: ").split()]
        print("Enter matrix:")
        matrix = [[float(x) for x in input().split()] for _ in range(row_col[0])]
        res = Matrix.recursive_determinant(matrix)
        print("The result is:\n" + str(float(res)) + "\n")

    @staticmethod
    def recursive_determinant(matrix: list):
        if len(matrix) == 1:
            return matrix[0][0]
        if len(matrix) == 2:
            return Matrix.determinant_2x2(matrix)
        d = 0.0
        for i in range(0, 1):
            for j in range(len(matrix[i])):
                d += (-1) ** (i + j) * matrix[i][j] * Matrix.det_space(i, j, matrix)

        return d

    @staticmethod
    def inverse_recursive_det(row, col, matrix: list):
        if len(matrix) == 1:
            return matrix[0][0]
        if len(matrix) == 2:
            return Matrix.determinant_2x2(matrix)

        d = 0.0
        for i in range(0, 1):
            for j in range(col, col + 1):
                d = (-1) ** (row + col) * Matrix.det_space(row, col, matrix)
        return d

    @staticmethod
    def print_inverse(total_matrix):
        print("The result is:")
        for i in range(len(total_matrix)):
            for j in range(len(total_matrix[0])):
                if total_matrix[i][j] < 0:
                    print((ceil(total_matrix[i][j] * 100) / 100.0), end=" ")
                else:
                    print((floor(total_matrix[i][j] * 100) / 100.0), end=" ")
            print()
        print()

    @staticmethod
    def det_space(row, col, matrix: list):
        if len(matrix) == 2:
            return Matrix.determinant_2x2(matrix)

        new_matrix = [[None for _ in range(len(matrix))] for _ in range(len(matrix))]
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if row == i or col == j:
                    continue
                else:
                    new_matrix[i][j] = matrix[i][j]

        for item in new_matrix:
            if all([x is None for x in item]):
                new_matrix.remove(item)

        new_matrix = [[x for x in item if x is not None] for item in new_matrix]
        if len(new_matrix) > 2:
            return Matrix.recursive_determinant(new_matrix)
        else:
            return Matrix.det_space(row, col, new_matrix)

    @staticmethod
    def determinant_2x2(matrix: list):
        return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])

    @staticmethod
    def inverse_matrix_menu():
        row_col = [int(x) for x in input("Enter matrix size: ").split()]
        print("Enter matrix:")
        matrix = [[float(x) for x in input().split()] for _ in range(row_col[0])]
        det_matrix = Matrix.recursive_determinant(matrix)
        if det_matrix == 0:
            print("This matrix doesn't have an inverse.\n")
            return 1
        new_matrix = Matrix.inverse_matrix(matrix)
        adjoint_matrix = Matrix.inverse_transpose(new_matrix)
        inverse_matrix = Matrix.multiply_inverse(adjoint_matrix, (1 / det_matrix))
        Matrix.print_inverse(inverse_matrix)

    @staticmethod
    def multiply_inverse(matrix: list, value):
        new_matrix = [[0 for _ in range(len(matrix))] for _ in range(len(matrix))]
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                new_matrix[i][j] = value * matrix[i][j]

        return new_matrix

    @staticmethod
    def inverse_transpose(matrix: list):
        new_matrix = [[0 for _ in range(len(matrix))] for _ in range(len(matrix))]

        for i in range(len(new_matrix)):
            for j in range(len(new_matrix[0])):
                new_matrix[i][j] = matrix[j][i]

        return new_matrix

    @staticmethod
    def inverse_matrix(matrix: list):
        new_matrix = [[None for _ in range(len(matrix))] for _ in range(len(matrix))]
        for i in range(len(new_matrix)):
            for j in range(len(new_matrix[i])):
                new_matrix[i][j] = Matrix.inverse_recursive_det(i, j, matrix)

        return new_matrix

    def menu(self):
        while True:
            print("1. Add matrices")
            print("2. Multiply matrix by a constant")
            print("3. Multiply matrices")
            print("4. Transpose matrix")
            print("5. Calculate a determinant")
            print("6. Inverse matrix\n0. Exit")
            choice = int(input("Your choice: "))
            if choice == 1:
                Matrix.run_total(self)
            elif choice == 2:
                Matrix.run_multiply_number()
            elif choice == 3:
                Matrix.run_multiply_matrix(self)
            elif choice == 4:
                Matrix.run_transpose()
            elif choice == 5:
                Matrix.menu_determinant()
            elif choice == 6:
                Matrix.inverse_matrix_menu()
            elif choice == 0:
                break


def main():
    matrix = Matrix()
    matrix.menu()


if __name__ == "__main__":
    main()
