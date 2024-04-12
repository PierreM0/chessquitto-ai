import copy
from typing import List, Tuple

board = [[None for j in range(4)] for i in range(4)]


class PionDeBase:
    def __init__(self, ligne: int, colonne: int, joueur: int, value: int, nom: str) -> None:
        self.ligne = ligne
        self.colonne = colonne
        self.joueur = joueur
        self.value = value
        self.nom = nom

    def get_moves(self, board):
        pass


def newBoard():
    return [[None for _ in range(4)] for _ in range(4)]


class Joueur:
    def __init__(self, numero: int):
        self.njoueur = numero
        self.pieces = []

    def enleverPiece(self, piece: PionDeBase) -> None:
        i = 0
        for p in self.pieces:
            if p.nom == piece.nom:
                self.pieces.pop(i)
                break
            i += 1

    def getScore(self) -> int:
        score = 0
        for p in self.pieces:
            score += p.value
        return score


class Board:
    def __init__(self, joueur1: Joueur, joueur2: Joueur):
        self.nligne = 4
        self.ncol = 4
        self.tab = newBoard()
        self.joueur1 = joueur1
        self.joueur2 = joueur2

    def get(self, pos: Tuple[int, int]) -> PionDeBase:
        return self.tab[pos[0]][pos[1]]

    # ATTENTION QUAND ON EST A LA PHASE UNE IL FAUT UTILISER CA !!!!

    def set(self, piece: PionDeBase, pos: (int, int)) -> None:
        if piece is not None:
            piece.ligne = pos[0]
            piece.colonne = pos[1]
        self.tab[pos[0]][pos[1]] = piece

    # Pour bouger une piece on utilise ça
    def Move(self, piece: PionDeBase, pos: (int, int)) -> None:
        oldx = piece.ligne
        oldy = piece.colonne
        if self.get(pos) is not None:
            if self.get(pos).joueur == 1:
                self.joueur1.enleverPiece(self.get(pos))
            else:
                self.joueur2.enleverPiece(self.get(pos))
        self.set(piece, pos)
        self.set(None, (oldx, oldy))

    # juste pour print le board.
    def __str__(self):
        chaine = ""
        for i in range(4):
            for j in range(4):
                if self.get((i, j)) is None:
                    chaine += " - "
                else:
                    chaine += " " + self.get((i, j)).nom + str(self.get((i, j)).joueur) + " "
            chaine += "\n"
        return chaine


class Tour(PionDeBase):
    def __init__(self, ligne: int, colonne: int, joueur: int):
        super().__init__(ligne, colonne, joueur, 5, "T")

    def get_moves(self, board: Board):
        # on crée une liste vide
        coups_possible: List[Tuple[int, int]] = []
        # on regarde les X d'un coté.
        for i in range(self.ligne + 1, 4):
            # on récupère la pièce
            piece = board.get((self.ligne, i))
            # si c'est pas une case vide
            if piece is not None:
                # et qu'elle appartient à l'adversaire, on l'ajoute aux coups possibles.
                if piece.joueur != self.joueur:
                    coups_possible.append((self.ligne, i))
                # dans tout les cas, la tour ne peux pas voir à travers les pieces et la boucle se stop quand il y a
                # une piece sur son chemin.
                break
            # si c'est une case vide, la tour peux s'y déplacer tranquillement, donc on l'ajoute, et on continue la
            # boucle
            coups_possible.append((self.ligne, i))
        # pareil de l'autre coté et pour les y en dessous.
        for i in range(0, self.ligne):
            piece = board.get((self.ligne, i))
            if piece is not None:
                if piece.joueur != self.joueur:
                    coups_possible.append((self.ligne, i))
                break
            coups_possible.append((self.ligne, i))
        for j in range(self.colonne + 1, 4):
            piece = board.get((j, self.colonne))
            if piece is not None:
                if piece.joueur != self.joueur:
                    coups_possible.append((j, self.colonne))
                break
            coups_possible.append((j, self.colonne))
        for j in range(0, self.colonne):
            piece = board.get((j, self.colonne))
            if piece is not None:
                if piece.joueur != self.joueur:
                    coups_possible.append((j, self.colonne))
                break
            coups_possible.append((j, self.colonne))
        return coups_possible


class Fou(PionDeBase):
    def __init__(self, ligne: int, colonne: int, joueur: int):
        super().__init__(ligne, colonne, joueur, 3, "F")

    def get_moves(self, board: Board):
        coups_possible: List[Tuple[int, int]] = []
        # deplacement haut gauche
        for i in range(1, min(self.ligne, self.colonne) + 1):
            if self.colonne - i >= 0 and self.ligne - i >= 0:
                piece = board.get((self.ligne - i, self.colonne - i))
                if piece is not None:
                    if piece.joueur != self.joueur:
                        coups_possible.append((self.ligne - i, self.colonne - i))
                    break
                coups_possible.append((self.ligne - i, self.colonne - i))
            else:
                break
        # deplacement haut droite
        for i in range(1, min(4 - self.colonne, self.ligne) + 1):
            if self.colonne + i < 4 and self.ligne - i >= 0:
                piece = board.get((self.ligne - i, self.colonne + i))
                if piece is not None:
                    if piece.joueur != self.joueur:
                        coups_possible.append((self.ligne - i, self.colonne + i))
                    break
                coups_possible.append((self.ligne - i, self.colonne + i))
            else:
                break
        # deplacement bas gauche
        for i in range(1, min(self.colonne, 4 - self.ligne) + 1):
            if self.colonne - i >= 0 and self.ligne + i < 4:
                piece = board.get((self.ligne + i, self.colonne - i))
                if piece is not None:
                    if piece.joueur != self.joueur:
                        coups_possible.append((self.ligne + i, self.colonne - i))
                    break
                coups_possible.append((self.ligne + i, self.colonne - i))
            else:
                break
        # deplacement bas droite
        for i in range(1, min(4 - self.colonne, 4 - self.ligne) + 1):
            if self.colonne + i < 4 and self.ligne + i < 4:
                piece = board.get((self.colonne + i, self.ligne + i))
                if piece is not None:
                    if piece.joueur != self.joueur:
                        coups_possible.append((self.ligne + 1, self.colonne + 1))
                    break
                coups_possible.append((self.ligne + 1, self.colonne + 1))
            else:
                break
        return coups_possible


class Cavalier(PionDeBase):
    def __init__(self, ligne: int, colonne: int, joueur: int):
        super().__init__(ligne, colonne, joueur, 3, "C")

    def get_moves(self, board: Board):
        liste = [(self.ligne + 1, self.colonne + 2), (self.ligne + 1, self.colonne - 2),
                 (self.ligne - 1, self.colonne + 2), (self.ligne - 1, self.colonne - 2),
                 (self.ligne + 2, self.colonne + 1), (self.ligne + 2, self.colonne - 1),
                 (self.ligne - 2, self.colonne + 1), (self.ligne - 2, self.colonne - 1)]
        toRemove = []
        for move in liste:
            if move[0] < 0 or move[1] < 0 or move[0] > 3 or move[1] > 3:
                toRemove.append(move)
            else:
                piece = board.get(move)
                if piece is not None:
                    if piece.joueur == self.joueur:
                        toRemove.append(move)
        for move in toRemove:
            liste.remove(move)
        return liste


class Reine(PionDeBase):
    def __init__(self, ligne: int, colonne: int, joueur: int):
        super().__init__(ligne, colonne, joueur, 9, "Q")

    def get_moves(self, board: Board):
        coups_possible: List[Tuple[int, int]] = []
        # deplacement haut gauche
        for i in range(1, min(self.ligne, self.colonne) + 1):
            if self.colonne - i >= 0 and self.ligne - i >= 0:
                piece = board.get((self.ligne - i, self.colonne - i))
                if piece is not None:
                    if piece.joueur != self.joueur:
                        coups_possible.append((self.ligne - i, self.colonne - i))
                    break
                coups_possible.append((self.ligne - i, self.colonne - i))
            else:
                break
        # deplacement haut droite
        for i in range(1, min(4 - self.colonne, self.ligne) + 1):
            if self.colonne + i < 4 and self.ligne - i >= 0:
                piece = board.get((self.ligne - i, self.colonne + i))
                if piece is not None:
                    if piece.joueur != self.joueur:
                        coups_possible.append((self.ligne - i, self.colonne + i))
                    break
                coups_possible.append((self.ligne - i, self.colonne + i))
            else:
                break
        # deplacement bas gauche
        for i in range(1, min(self.colonne, 4 - self.ligne) + 1):
            if self.colonne - i >= 0 and self.ligne + i < 4:
                piece = board.get((self.ligne + i, self.colonne - i))
                if piece is not None:
                    if piece.joueur != self.joueur:
                        coups_possible.append((self.ligne + i, self.colonne - i))
                    break
                coups_possible.append((self.ligne + i, self.colonne - i))
            else:
                break
        # deplacement bas droite
        for i in range(1, min(4 - self.colonne, 4 - self.ligne) + 1):
            if self.colonne + i < 4 and self.ligne + i < 4:
                piece = board.get((self.colonne + i, self.ligne + i))
                if piece is not None:
                    if piece.joueur != self.joueur:
                        coups_possible.append((self.ligne + 1, self.colonne + 1))
                    break
                coups_possible.append((self.ligne + 1, self.colonne + 1))
            else:
                break
        for i in range(self.ligne + 1, 4):
            # on récupère la pièce
            piece = board.get((self.ligne, i))
            # si c'est pas une case vide
            if piece is not None:
                # et qu'elle appartient à l'adversaire, on l'ajoute aux coups possibles.
                if piece.joueur != self.joueur:
                    coups_possible.append((self.ligne, i))
                # dans tout les cas, la tour ne peux pas voir à travers les pieces et la boucle se stop quand il y a
                # une piece sur son chemin.
                break
            # si c'est une case vide, la tour peux s'y déplacer tranquillement, donc on l'ajoute, et on continue la
            # boucle
            coups_possible.append((self.ligne, i))
        # pareil de l'autre coté et pour les y en dessous.
        for i in range(0, self.ligne):
            piece = board.get((self.ligne, i))
            if piece is not None:
                if piece.joueur != self.joueur:
                    coups_possible.append((self.ligne, i))
                break
            coups_possible.append((self.ligne, i))
        for j in range(self.colonne + 1, 4):
            piece = board.get((j, self.colonne))
            if piece is not None:
                if piece.joueur != self.joueur:
                    coups_possible.append((j, self.colonne))
                break
            coups_possible.append((j, self.colonne))
        for j in range(0, self.colonne):
            piece = board.get((j, self.colonne))
            if piece is not None:
                if piece.joueur != self.joueur:
                    coups_possible.append((j, self.colonne))
                break
            coups_possible.append((j, self.colonne))
        return coups_possible


if __name__ == '__main__':
    tourJ1 = Tour(-1, -1, 1)
    tourJ2 = Tour(-1, -1, 2)
    fouJ1 = Fou(-1, -1, 1)
    fouJ2 = Fou(-1, -1, 2)
    joueur = Joueur(1)
    joueur.pieces.append(tourJ1)
    joueur.pieces.append(fouJ1)
    joueur2 = Joueur(2)
    joueur2.pieces.append(tourJ2)
    joueur2.pieces.append(fouJ2)
    board = Board(joueur, joueur2)
    board.set(tourJ1, (0, 0))
    board.set(tourJ2, (2, 2))
    board.set(fouJ1, (1, 1))
    board.set(fouJ2, (2, 3))
    cav1 = Cavalier(-1, -1, 1)
    joueur.pieces.append(cav1)
    board.set(cav1, (0, 3))
    reine = Reine(-1,-1,1)
    joueur.pieces.append(reine)
    board.set(reine,(3,3))
    print(board)
    print(reine.get_moves(board))
    board.Move(tourJ1, (2, 2))
    print(board)
