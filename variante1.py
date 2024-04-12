import copy
import math
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
        self.deplacementsSansPrises = 0
        self.piecesJoueur1APlacer = [Reine(-1, -1, 1), Tour(-1, -1, 1), Cavalier(-1, -1, 1), Fou(-1, -1, 1)]
        self.piecesJoueur2APlacer = [Reine(-1, -1, 2), Tour(-1, -1, 2), Cavalier(-1, -1, 2), Fou(-1, -1, 2)]
        self.phase = 1

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
            self.deplacementsSansPrises = 0
        else:
            self.deplacementsSansPrises += 1
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


def valuerJeu(board: Board):
    score = board.joueur2.getScore() - board.joueur1.getScore()
    return score


def gagner(board: Board):
    if(board.phase == 1):
        return 0
    if len(board.joueur1.pieces) == 0:
        return 1  # ia gagne donc bonne valeur.
    if len(board.joueur2.pieces) == 0:
        return -1  # joueur gagne donc mauvaise valeur
    # sinon on regarde si on a atteint le nb de déplacements sans capturer max
    if board.deplacementsSansPrises == 5:
        if board.joueur1.getScore() > board.joueur2.getScore():
            return -1
        else:
            return 1
    return 0


def jouer(board: Board, nom: str, pos: Tuple[int, int], njoueur: int):
    nboard = copy.deepcopy(board)
    if njoueur == 1:
        for piece in nboard.joueur1.pieces:
            if piece.nom == nom:
                nboard.Move(piece, pos)
    else:
        for piece in nboard.joueur2.pieces:
            if piece.nom == nom:
                nboard.Move(piece, pos)
    return nboard


def placer(board: Board, nom: str, pos: Tuple[int, int], njoueur: int):
    nboard = copy.deepcopy(board)
    if njoueur == 1:
        for piece in nboard.piecesJoueur1APlacer:
            if piece.nom == nom:
                nboard.joueur1.pieces.append(piece)
                nboard.set(piece, pos)
                nboard.piecesJoueur1APlacer.remove(piece)
    else:
        for piece in nboard.piecesJoueur2APlacer:
            if piece.nom == nom:
                nboard.joueur2.pieces.append(piece)
                nboard.set(piece, pos)
                nboard.piecesJoueur2APlacer.remove(piece)
    if len(nboard.piecesJoueur2APlacer) == 0 and len(nboard.piecesJoueur1APlacer) ==0:
        nboard.phase = 2
    return nboard


def valMax(board, alpha, beta, depth):
    # si on atteind le max on s'arrête
    if depth == 0:
        return valuerJeu(board), (-1, -1),"Z"
    # on regarde si la partie est finie
    if gagner(board) == 1:
        return 50, (-1, -1),"Z"
    if gagner(board) == -1:
        return -50, (-1, -1),"Z"

    scoreMax = -100
    coupMax = (-1, -1)
    lettreMax = "Z"
    # liste des coups possibles pour l'IA
    if (board.phase == 1):
        placementPossibles = []
        for i in range(4):
            for j in range(4):
                if board.get((i, j)) is None:
                    placementPossibles.append((i, j))
        for piece in board.piecesJoueur2APlacer:
            for pos in placementPossibles:
                valeurs = valMin(placer(board, piece.nom, pos, 2), alpha, beta, depth - 1)
                score = valeurs[0]
                coup = valeurs[1]
                if score > scoreMax:
                    scoreMax = score
                    coupMax = pos
                    lettreMax = piece.nom
                if (scoreMax >= beta):
                    return scoreMax, coupMax,lettreMax
                alpha = max(alpha, scoreMax)
    else:
        for piece in board.joueur2.pieces:
            for move in piece.get_moves(board):
                valeurs = valMin(jouer(board, piece.nom, move, 2), alpha, beta, depth - 1)
                score = valeurs[0]
                coup = valeurs[1]
                if score > scoreMax:
                    scoreMax = score
                    coupMax = move
                    lettreMax = piece.nom
                if (scoreMax >= beta):
                    return scoreMax, coupMax,lettreMax
                alpha = max(alpha, scoreMax)
    return scoreMax, coupMax,lettreMax


def valMin(board, alpha, beta, depth):
    # si on atteind le max on s'arrête
    if depth == 0:
        return valuerJeu(board), (-1, -1),"Z"
    # on regarde si la partie est finie
    if gagner(board) == 1:
        return 50, (-1, -1),"Z"
    if gagner(board) == -1:
        return -50, (-1, -1),"Z"

    scoreMin = 100
    coupMin = (-1, -1)
    lettreMin = "Z"
    if (board.phase == 1):
        placementPossibles = []
        for i in range(4):
            for j in range(4):
                if board.get((i, j)) is None:
                    placementPossibles.append((i, j))
        for piece in board.piecesJoueur1APlacer:
            for pos in placementPossibles:
                valeurs = valMax(placer(board,piece.nom,pos,1),alpha,beta,depth-1)
                score = valeurs[0]
                coup = valeurs[1]
                if score < scoreMin:
                    scoreMin = score
                    coupMin = pos
                    lettreMin = piece.nom
                if (alpha >= scoreMin):
                    return scoreMin, coupMin,lettreMin
                beta = min(beta, scoreMin)
    else:
        for piece in board.joueur1.pieces:
            for move in piece.get_moves(board):
                valeurs = valMax(jouer(board, piece.nom, move, 1), alpha, beta,depth-1)
                score = valeurs[0]
                coup = valeurs[1]
                if score < scoreMin:
                    scoreMin = score
                    coupMin = move
                    lettreMin = piece.nom
                if (alpha >= scoreMin):
                    return scoreMin, coupMin,lettreMin
                beta = min(beta, scoreMin)

    return scoreMin, coupMin,lettreMin

def jouerPartie():
    board = Board(Joueur(1),Joueur(2))
    print("début du jeu !")
    while( gagner(board) == 0 or board.phase == 1):
        if board.phase == 1:
            print(board)
            print("il faut placer vos pieces : TAPEZ LE NOM DE LA PIECE (Q,T,F,C) parmis les pieces qu'il vous reste à placer")
            for piece in board.piecesJoueur1APlacer:
                print(piece.nom+" " , end="")
            lettre = str(input("rentrez une lettre :"))
            ligne = int(input("rentrez la ligne:"))
            colonne = int(input("rentrez la colonne:"))
            board = placer(board, lettre, (ligne,colonne), 1)
            print(board)
            _,IA_play,lettre_ia = valMax(board,-math.inf,math.inf,4)
            if(IA_play == (-1,-1)):
                print(board)
                break
            board = placer(board,lettre_ia,IA_play,2)
            print("L'IA a joué : "+lettre_ia+" ligne : "+str(IA_play[0])+"colonne: "+str(IA_play[1]))
        else:
            print("PHASE DE JEU !")
            print(board)
            print("il faut placer vos pieces : TAPEZ LE NOM DE LA PIECE (Q,T,F,C) qu'il vous reste !")
            for piece in board.joueur1.pieces:
                print(piece.nom+" ", end="")
            lettre = str(input("rentrez une lettre :"))
            ligne = int(input("rentrez la ligne:"))
            colonne = int(input("rentrez la colonne:"))
            board = jouer(board, lettre, (ligne,colonne), 1)
            print(board)
            _,IA_play,lettre_ia = valMax(board,-math.inf,math.inf,4)
            if(IA_play == (-1,-1)):
                print(board)
                break
            board = jouer(board,lettre,IA_play,2)
            print(board)
            print("L'IA a joué : " + lettre_ia + " ligne : " + str(IA_play[0]) + "colonne: " + str(IA_play[1]))
    if(gagner(board) == 1):
        print("vous avez perdu !")
    else:
        print("vous avez gagné !")
if __name__ == '__main__':
    jouerPartie()
