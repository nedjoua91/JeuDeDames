from tkinter import *
from math import *
import random
import time


# Définition des gestionnaires d'événements :

def damier():   # Création du damier
    a = 50
    b = 0
    c = 1
    for i in range(1, 51):
        can1.create_rectangle(a, b, a+50, b+50, width=2, fill='#8B4513')    # Marron foncé
        a += 100
        if a == 550:
            a = 0
            b += 50
            c += 1
        if a == 500:
            a = 50
            b += 50
            c += 1
    
    a = 0
    b = 0
    for i in range(51, 101):
        can1.create_rectangle(a, b, a+50, b+50, width=2, fill='#DEB887')    # Marron clair
        a += 100
        if a == 550:
            a = 0
            b += 50
            c += 1
        if a == 500:
            a = 50
            b += 50
            c += 1

def pions():    # Création des pions
    a = 60
    b = 10
    for i in range(0, 40):
        if i in range (0, 20):
            can1.create_oval(a, b, a+30, b+30, width=2, fill='black', tags = "computer")
        else:
            can1.create_oval(a, b, a+30, b+30, width=2, fill='white', tags = "human")
        a += 100
        if a == 560:
            a = 10
            b += 50
        if a == 510:
            a = 60
            b += 50
        if b == 210:
            a = 60
            b += 100


class Dames:
    """ A state of the game, i.e. the game board.
        Squares in the board are in this arrangement
        51 01 52 02 53 03 54 04 55 05
        06 56 07 57 08 58 09 59 10 60
        61 11 62 12 63 13 64 14 65 15
        16 66 17 67 18 68 19 69 20 70
        71 21 72 22 73 23 74 24 75 25
        26 76 27 77 28 78 29 79 30 80
        81 31 82 32 83 33 84 34 85 35
        36 86 37 87 38 88 39 89 40 90
        91 41 92 42 93 43 94 44 95 45
        46 96 47 97 48 98 49 99 50 100
        where 0 = empty, 1 = player 1 (Human), 2 = player 2 (Computer)
    """
    def __init__(self):
        self.playerJustMoved = 2 # At the root pretend the player just moved is p2 - p1 has the first move
        self.board = [0] + [2]*20 + [0]*10 + [1]*20
        
    
    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = Dames()
        st.playerJustMoved = self.playerJustMoved
        st.board = self.board[:]
        return st
    
    def DoMove(self,move):
        """ Update a state by carrying out the given move.
            Must update playerToMove.
        """
        self.playerJustMoved = 3 - self.playerJustMoved

        if len(move) == 2:
            self.board[move[0]] = 0
            self.board[move[1]] = self.playerJustMoved          
    
        elif len(move)%2 == 1:
            move2 = list(move)
            while len(move2) != 1:
                self.board[move2[0]] = 0
                self.board[move2[1]] = 0
                self.board[move2[2]] = self.playerJustMoved
                move2.pop(0)
                move2.pop(0)
    
    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        coups = []
        if   self.playerJustMoved == 1:
            tag = "computer"
            preneur = 2
            prise = 1   # Pourrait utiliser playerJustMoved
        elif self.playerJustMoved == 2:
            tag = "human"
            preneur = 1
            prise = 2   # Pourrait utiliser playerJustMoved
            
        # Rechercher prise obligatoire
        board = self.board.copy()
        for i in range(1,len(board)):
             state.GetMoves2(i, coups, board, self.playerJustMoved)
             
        for i in coups:
            board = self.board.copy()
            board[i[0]] = 0
            board[i[1]] = 0
            board[i[2]] = 3 - self.playerJustMoved

            doge = False
            for z in coups:
                if coups.count(z) >= 2:
                    doge = True
            if doge == False:
                state.GetMoves2(i[2], coups, board, self.playerJustMoved)
            else:
                "Do nothing"
            
        # Traiter la liste...
        test = list(coups)
        for a in coups:
            for b in test:
                if set(b).issubset(a):
                    "Do nothing"
                elif a[-1] == b[0]:
                    c = list(b)
                    c.pop(0)
                    g = []
                    g = a + c
                    coups.append(g)
        
        # Traiter la liste, en enlevant les petits coups
        big = 0
        for d in list(coups):
            if len(d) > big:
                big = len(d)

        for d in list(coups):
            if big > len(d):
                coups.remove(d)
            else:
                "Do nothing"
        
        if coups == []: # S'il n'existe pas de prise réalisable, rechercher les déplacements possibles
            for i in range(1,len(self.board)):
                if tag == "human" and i > 5 and self.board[i] == 1:
                    if self.board[i-5] == 0:
                        coups.append([i,i-5])
                    if i % 10 == 5 or i % 10 == 6:
                        "Do nothing"
                    elif i % 10 == 0:
                        if self.board[i-6] == 0:
                            coups.append([i,i-6])
                    elif (i % 10) - 5 < 0:
                        if self.board[i-4] == 0:
                            coups.append([i,i-4])
                    elif (i % 10) - 5 > 0:
                        if self.board[i-6] == 0:
                            coups.append([i,i-6])
                
                elif tag == "computer" and i < 46 and self.board[i] == 2: 
                    if self.board[i+5] == 0:
                        coups.append([i,i+5])
                    if i % 10 == 6 or i % 10 == 5:
                        "Do nothing"
                    elif i % 10 == 0:
                        if self.board[i+4] == 0:
                            coups.append([i,i+4])
                    elif (i % 10) - 5 < 0:
                        if self.board[i+6] == 0:
                            coups.append([i,i+6])
                    elif (i % 10) - 5 > 0:
                        if self.board[i+4] == 0:
                            coups.append([i,i+4])
        
        return coups

    def GetMoves2(self, i, coups, board, pJM): # Pas optimale, pourrait donner des erreurs, à tester
        """ Get all possible moves from this state.
        """
        if   pJM == 1:
            preneur = 2
            prise = 1   # Pourrait utiliser playerJustMoved
        elif pJM == 2:
            preneur = 1
            prise = 2   # Pourrait utiliser playerJustMoved
        
        if i%10 - 6 < 0 and i%10 !=0:
            col = "impair"
        elif i%10 - 6 >= 0 or i%10 == 0:
            col = "pair"
        
        if i == 1 and board[i] == preneur and board[i+6] == prise and board[i+11] == 0:
            coups.append([i,i+6,i+11])
        elif i == 6 and board[i] == preneur and board[i+5] == prise and board[i+11] == 0:
            coups.append([i,i+5,i+11])
        elif i == 5 and board[i] == preneur and board[i+5] == prise and board[i+9] == 0:
            coups.append([i,i+5,i+9])
        elif i == 10 and board[i] == preneur and board[i+4] == prise and board[i+9] == 0:
            coups.append([i,i+4,i+9])
        elif i == 45 and board[i] == preneur and board[i-5] == prise and board[i-11] == 0:
            coups.append([i,i-5,i-11])
        elif i == 50 and board[i] == preneur and board[i-6] == prise and board[i-11] == 0:
            coups.append([i,i-6,i-11])
        elif i == 46 and board[i] == preneur and board[i-5] == prise and board[i-9] == 0:
            coups.append([i,i-5,i-9])
        elif i == 41 and board[i] == preneur and board[i-4] == prise and board[i-9] == 0:
            coups.append([i,i-4,i-9])
        elif i == 16 or i == 26 or i == 36:
            if board[i] == preneur and board[i-5] == prise and board[i-9] == 0:
                coups.append([i,i-5,i-9])
            if board[i] == preneur and board[i+5] == prise and board[i+11] == 0:
                coups.append([i,i+5,i+11])
        elif i == 11 or i == 21 or i == 31:
            if board[i] == preneur and board[i-4] == prise and board[i-9] == 0:
                coups.append([i,i-4,i-9])
            if board[i] == preneur and board[i+6] == prise and board[i+11] == 0:
                coups.append([i,i+6,i+11])
        elif i == 20 or i == 30 or i == 40:
            if board[i] == preneur and board[i-6] == prise and board[i-11] == 0:
                coups.append([i,i-6,i-11])
            if board[i] == preneur and board[i+4] == prise and board[i+9] == 0:
                coups.append([i,i+4,i+9])
        elif i == 15 or i == 25 or i == 35:
            if board[i] == preneur and board[i-5] == prise and board[i-11] == 0:
                coups.append([i,i-5,i-11])
            if board[i] == preneur and board[i+5] == prise and board[i+9] == 0:
                coups.append([i,i+5,i+9])
        elif i == 2 or i == 3 or i == 4:
            if board[i] == preneur and board[i+5] == prise and board[i+9] == 0:
                coups.append([i,i+5,i+9])
            if board[i] == preneur and board[i+6] == prise and board[i+11] == 0:
                coups.append([i,i+6,i+11])
        elif i == 7 or i == 8 or i == 9:
            if board[i] == preneur and board[i+4] == prise and board[i+9] == 0:
                coups.append([i,i+4,i+9])
            if board[i] == preneur and board[i+5] == prise and board[i+11] == 0:
                coups.append([i,i+5,i+11])
        elif i == 42 or i == 43 or i == 44:
            if board[i] == preneur and board[i-5] == prise and board[i-11] == 0:
                coups.append([i,i-5,i-11])
            if board[i] == preneur and board[i-4] == prise and board[i-9] == 0:
                coups.append([i,i-4,i-9])
        elif i == 47 or i == 48 or i == 49:
            if board[i] == preneur and board[i-6] == prise and board[i-11] == 0:
                coups.append([i,i-6,i-11])
            if board[i] == preneur and board[i-5] == prise and board[i-9] == 0:
                coups.append([i,i-5,i-9])
        elif i > 11 and i < 40 and i%5!=0 and i%5 !=1:
            if col == "pair": # noir
                if board[i] == preneur and board[i-5] == prise and board[i-9] == 0:
                    coups.append([i,i-5,i-9])
                if board[i] == preneur and board[i+5] == prise and board[i+11] == 0:
                    coups.append([i,i+5,i+11])
                if board[i] == preneur and board[i+4] == prise and board[i+9] == 0:
                    coups.append([i,i+4,i+9])
                if board[i] == preneur and board[i-6] == prise and board[i-11] == 0:
                    coups.append([i,i-6,i-11])
            if col == "impair": # rouge
                if board[i] == preneur and board[i-4] == prise and board[i-9] == 0:
                    coups.append([i,i-4,i-9])
                if board[i] == preneur and board[i+6] == prise and board[i+11] == 0:
                    coups.append([i,i+6,i+11])
                if board[i] == preneur and board[i+5] == prise and board[i+9] == 0:
                    coups.append([i,i+5,i+9])
                if board[i] == preneur and board[i-5] == prise and board[i-11] == 0:
                    coups.append([i,i-5,i-11])
        
        return coups
    
    def GetResult(self, playerjm):  # playerjm est inutile ? seulement une IA
        """ Get the game result from the viewpoint of playerjm. 
        """
        piece_human = 0
        piece_computer = 0
        for i in range (1,51):
            if self.board[i] == 1:
                piece_human += 1
            elif self.board[i] == 2:
                piece_computer += 1
        
        if piece_human == piece_computer:
            return 0.5
        elif piece_human > piece_computer:
            return 0
        elif piece_human < piece_computer:
            return 1
    
    def __repr__(self):
        s= ""
        for i in range(1,51):
            if i % 10 == 1:
                s += "."
            s += ".XO"[self.board[i]]
            if i % 10 != 5:
                s += "."
            if i % 10 == 5: s += "\n"
            if i % 10 == 0: s += "\n"
        return s


class Node: # à modifier...
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves() # future child nodes
        self.playerJustMoved = state.playerJustMoved # the only part of the state that the Node needs later
        
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s
    
    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""
    
    rootnode = Node(state = rootstate)
    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()
        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)
        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m,state) # add child and descend tree
        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []: # while state is non-terminal
            state.DoMove(random.choice(state.GetMoves()))
        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(node.playerJustMoved)) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode
    # Output some information about the tree - can be omitted
    if (verbose): print (rootnode.TreeToString(0))
    else: print (rootnode.ChildrenToString())

    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited
 

def simulation():
    global flag, compteur
    while state.GetMoves() != []:
        if flag == 0:
            compteur += 1
            coups = state.GetMoves()
            m = random.choice(coups)
            deplacement_pion(m)
            state.DoMove(m)                             # Actualisation
            flag = 1
        elif flag == 1:
            computer(flag)
        fen1.update()
        time.sleep(0.5)
    draw(flag)

def computer(e):
    global flag, compteur
    if flag == 1:
        "C'est le tour des noirs !"
        compteur += 1
        if state.GetMoves() != []:
            print("Coups possibles de l'ordinateur :", state.GetMoves())
            m = UCT(rootstate = state, itermax = 100, verbose = True) #...
            print("Best move :", m)
            deplacement_pion(m)    # déplacer un pion
            state.DoMove(m)                             # Actualisation
        else:
            print("L'ordinateur passe son tour")
            draw(flag)
        "Fin du tour des noirs !"
        flag = 0
        print("Coups possibles :", state.GetMoves())
    else:
        "Ça n'est pas le tour des noirs"

def deplacement_pion(m):    # Déplacement sur l'interface graphique
    move = list(m)
    coords = can1.coords(move[0])
    x0 = coords[0]
    y0 = coords[1]
    x1 = coords[2]
    y1 = coords[3]
    hunter = can1.find_enclosed(x0-5,y0-5,x1-5,y1-5)

    coords = can1.coords(move[1])                      # Récupération des coordonnées du pion qui sera pris
    x0 = coords[0]
    y0 = coords[1]
    x1 = coords[2]
    y1 = coords[3]
    
    if len(move) == 2:
        can1.coords(hunter,x0+10,y0+10,x1-10,y1-10) # Déplacement du pion effectuant la prise
        print(compteur,":",move[0],"-",move[1],"\n")           # Notation Manoury du coup joué

    elif len(move) > 2:
        manoury = str(compteur) + " : " + str(move[0])
        while len(move) != 1:
            target = can1.find_enclosed(x0-5,y0-5,x1-5,y1-5)

            coords = can1.coords(move[2])                  # 
            x0 = coords[0]
            y0 = coords[1]
            x1 = coords[2]
            y1 = coords[3]
             
            can1.coords(hunter,x0+10,y0+10,x1-10,y1-10) # Déplacement du pion effectuant la prise
            can1.delete(target)                         # Suppression du pion pris
            fen1.update()
            time.sleep(0.5)
            manoury += " x " + str(move[2])
            move.pop(0)
            move.pop(0)
            if len(move) != 1:
                coords = can1.coords(move[0])
                x0 = coords[0]
                y0 = coords[1]
                x1 = coords[2]
                y1 = coords[3]
                hunter = can1.find_enclosed(x0-5,y0-5,x1-5,y1-5)

                coords = can1.coords(move[1])                      # Récupération des coordonnées du pion qui sera pris
                x0 = coords[0]
                y0 = coords[1]
                x1 = coords[2]
                y1 = coords[3]

        print(manoury + "\n")
                
    else:
        "Impossible"

def human(e): # Il y a peut-être des erreurs, à tester !
    global deplacement, jeton, compteur, flag, coups, move0, move2, prisetable, manoury, issubset, isequal
    if state.GetMoves() != []:
        if flag == 0:
            "C'est le tour des blancs !"
            
            if compteur % 2 == 0:
                compteur += 1
            
            if deplacement == 0: # Au premier clic, on récupère les coordonnées de la souris et l'identifiant du pion sélectionné s'il y en a un
                coups = state.GetMoves()

                x0 = int(e.x/50)*50 # Abscisse du coin supérieur gauche de la case
                y0 = int(e.y/50)*50 # Ordonnée du coin supérieur gauche de la case

                move0 = can1.find_enclosed(x0-5,y0-5,x0+55,y0+55) # Récupère l'id de la case
                move0 = move0[0]
                manoury = str(compteur) + " : " + str(move0)
                for i in list(coups):
                    if move0 == i[0]:
                        deplacement = 1
                        jeton = can1.find_enclosed(x0+5,y0+5,x0+45,y0+45)
                        jeton = jeton[0]
                    else:
                        coups.remove(i)

                prisetable = [move0]
                
            elif deplacement == 1: # Au second clic, on récupère les coordonnées de la souris et la destination
                x0 = int(e.x/50)*50 # Abscisse du coin supérieur gauche de la case
                y0 = int(e.y/50)*50 # Ordonnée du coin supérieur gauche de la case
                
                move2 = can1.find_enclosed(x0-5,y0-5,x0+55,y0+55) # Récupère l'id de la case
                move2 = move2[0]

                prisetable.append(move2)
                if len(coups[0]) < 3:
                    if [move0,move2] in coups:
                        can1.coords(jeton,x0+10,y0+10,x0+40,y0+40)
                        print(compteur,":",move0,"-",move2,"\n")
                        move = [move0, move2]
                        state.DoMove(move)
                        deplacement = 0
                        flag = 1
                    else:
                        "Déplacement impossible"
                    issubset = False
                elif len(coups[0]) > 2: # Prise obligatoire multiple
                    a = 0
                    for i in list(coups):
                        if set(prisetable).issubset(i):
                            issubset = True
                            
                        else:
                            a += 1

                    if a == len(list(coups)):
                        issubset = False
                    
                    if issubset == False:
                        deplacement = 0
                    isequal = False
                    for i in list(coups):
                        if prisetable == i:
                            isequal = True
                            move = i
                        else:
                            "Nothing"

                    if isequal == True:
                        while len(prisetable) != 1:
                            
                            coords = can1.coords(prisetable[0])
                            x0 = coords[0]
                            y0 = coords[1]
                            x1 = coords[2]
                            y1 = coords[3]
                            hunter = can1.find_enclosed(x0-5,y0-5,x1-5,y1-5)

                            coords = can1.coords(prisetable[1])                      # Récupération des coordonnées du pion qui sera pris
                            x0 = coords[0]
                            y0 = coords[1]
                            x1 = coords[2]
                            y1 = coords[3]
                            target = can1.find_enclosed(x0-5,y0-5,x1-5,y1-5)

                            coords = can1.coords(prisetable[2])                  # 
                            x0 = coords[0]
                            y0 = coords[1]
                            x1 = coords[2]
                            y1 = coords[3]
                             
                            can1.coords(hunter,x0+10,y0+10,x1-10,y1-10) # Déplacement du pion effectuant la prise
                            can1.delete(target)                         # Suppression du pion pris
                            fen1.update()
                            time.sleep(0.5)
                            manoury += " x " + str(prisetable[2])
                            prisetable.pop(0)
                            prisetable.pop(0)
                        print(manoury + "\n")
                        state.DoMove(move)
                        deplacement = 0
                        flag = 1
                        
                    else:
                        "Déplacement impossible"
                    
                else:
                    "Impossible"
        else:
            "Pas votre tour"
    else:
        print("Le joueur passe son tour")
        draw(flag)   

def draw(e):
    global flag, gagnant
    piece_player1 = can1.find_withtag("human")
    piece_player2 = can1.find_withtag("computer")
    if len(piece_player1) == len(piece_player2):
        print("Match nul ! \n")
        gagnant = 0.5
    elif len(piece_player1) > len(piece_player2):
        print("Le joueur gagne ! \n")
        gagnant = 0
    elif len(piece_player1) < len(piece_player2):
        print("L'ordinateur gagne ! \n")
        gagnant = 1
    flag = 2
    return gagnant

def UCTPlayGame(sim):
    global flag, deplacement, compteur, fen1, can1, state
    #============= Programme principal =============

    # Les variables suivantes seront utilisées de manière globale :
    flag = 0        # 
    deplacement = 0 # Commutateurs
    compteur = 0    #

    # Création du widget principal ("parent") :
    fen1 = Tk()
    fen1.title("Jeu de dames")

    # Création des widgets "enfants" :
    can1 = Canvas(fen1, bg='dark grey', height=500, width=500)
    can1.pack(side=LEFT, padx=5, pady=5)

    damier()
    pions()

    state = Dames()
    print("Coups possibles :", state.GetMoves())

    if sim:
        simulation()
        return gagnant

    # Mouseclick event
    can1.bind("<Button 1>", human)
    can1.bind("<Button 2>", draw)
    can1.bind("<Button 3>", computer)

    bou1 = Button(fen1, text='Simulation', width=12, command=simulation)
    bou1.pack()

    # Démarrage du réceptionnaire d'évènements (boucle principale) :
    fen1.mainloop()

if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players. # à changer
    """
    UCTPlayGame(False)