from typing import List, Tuple

board = [[None for j in range(4)] for i in range(4)]


class PionDeBase:
    def __init__(self, x: int, y: int, color: bool, value: int) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.value = value

    def __str__(self):
        return f"PionDeBase({self.x}, {self}"

    def get_all_move(self) -> List[Tuple[int, int]]:
        pass

    def __get_bishop_move(self) -> List[Tuple[int, int]]:
        moves = []

        x = self.x
        y = self.y
        while x < 4 and y < 4 and board[x][y] is None:
            moves.append((x, y))

        x = self.x
        y = self.y
        while x > 0 and y > 0 and board[x][y] is None:
            moves.append((x, y))

        x = self.x
        y = self.y
        while x < 4 and y > 0 and board[x][y] is None:
            moves.append((x, y))

        x = self.x
        y = self.y
        while x > 0 and y < 4 and board[x][y] is None:
            moves.append((x, y))

        return moves

    def __get_rook_move(self) -> List[Tuple[int, int]]:
        moves = []

        x = self.x
        y = self.y
        while x < 4 and board[x][y] is None:
            moves.append((x, y))

        x = self.x
        y = self.y
        while y < 4 and board[x][y] is None:
            moves.append((x, y))

        x = self.x
        y = self.y
        while x > 0 and board[x][y] is None:
            moves.append((x, y))

        x = self.x
        y = self.y
        while y > 0 and board[x][y] is None:
            moves.append((x, y))

        return moves


def in_the_board(pos: Tuple[int, int], add: Tuple[int, int]) -> bool:
    x = pos[0] + add[0]
    y = pos[1] + add[1]
    #   Normalement c'est OK : la grille de jeu contient des None ou des PionDeBase
    return (x < 0 or y < 0 or x >= 4 or y >= 4 or
            (board[x][y] is not None and board[x][y].color == board[pos[0]][pos[1]].color))


class Qeen(PionDeBase):
    def __init__(self, x: int, y: int, color: bool) -> None:
        super().__init__(x, y, color, 5)

    def get_all_move(self) -> List[Tuple[int, int]]:
        return self.__get_bishop_move() + self.__get_rook_move()


class Rook(PionDeBase):
    def __init__(self, x: int, y: int, color: bool) -> None:
        super().__init__(x, y, color, 4)

    def get_all_move(self) -> List[Tuple[int, int]]:
        return self.__get_rook_move()


class Knight(PionDeBase):
    def __init__(self, x: int, y: int, color: bool) -> None:
        super().__init__(x, y, color, 3)

    def get_all_move(self) -> List[Tuple[int, int]]:
        moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        return filter(lambda move: in_the_board((self.x, self.y), move), moves)


class Bishop(PionDeBase):
    def __init__(self, x: int, y: int, color: bool) -> None:
        super().__init__(x, y, color, 2)

    def get_all_move(self) -> List[Tuple[int, int]]:
        return self.__get_bishop_move()


class King(PionDeBase):
    def __init__(self, x: int, y: int, color: bool) -> None:
        super().__init__(x, y, color, int("inf"))

    def get_all_move(self) -> List[Tuple[int, int]]:
        moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        return filter(lambda move: in_the_board((self.x, self.y), move), moves)


class Pawn(PionDeBase):
    def __init__(self, x: int, y: int, color: bool) -> None:
        super().__init__(x, y, color, 1)

    def get_all_move(self) -> List[Tuple[int, int]]:
        moves = []
        if in_the_board((self.x, self.y), (1, 0)) and board[self.x + 1][self.y] is None:
            moves.append((1, 0))
        if in_the_board((self.x, self.y), (-1, 0)) and board[self.x - 1][self.y] is None:
            moves.append((-1, 0))

        if (in_the_board((self.x, self.y), (-1, 1)) and board[self.x - 1][self.y + 1] is not None and
                board[self.x - 1][self.y + 1].color != self.color):
            moves.append((-1, 1))
        if (in_the_board((self.x, self.y), (1, 1)) and board[self.x + 1][self.y + 1] is not None and
                board[self.x + 1][self.y + 1].color != self.color):
            moves.append((1, 1))

        if (in_the_board((self.x, self.y), (-1, -1)) and board[self.x - 1][self.y - 1] is not None and
                board[self.x - 1][self.y - 1].color != self.color):
            moves.append((-1,-1))
        if (in_the_board((self.x, self.y), (1, -1)) and board[self.x + 1][self.y - 1] is not None and
                board[self.x + 1][self.y - 1].color != self.color):
            moves.append((1,-1))

        return moves

if __name__ == '__main__':
    pass