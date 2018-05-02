from collections import namedtuple
import random

"""
DEAR SARAH,
    
    I AM WRITING STUFF HERE NOW IN LETTER FORMAT. THERE ARE A BUNCH OF PLACES WHERE I PUT THAT
    I DID STUFF ASSUMING THAT BLOCK REQUIRES A COORDINATE. IF YOU WANT TO MAKE IT SO THAT BLOCK
    DOESN'T REQUIRE A COORDINATE, YOU MIGHT HAVE TO REDO THOSE PARTS (OR JUST FIND A WAY TO MAKE
    IT SO THAT BLOCK JUST COPIES THE COORDINATE OF AN OPPOSING TAKE, I LEAVE THE CHOICE TO YOU) 

    CAN YOU FIX YOUR CHECK_FOR_WINNER FUNCTION SO THAT THE TEST I WROTE IN THE OTHER FILE WORKS
    OR AT LEAST FAILS ON SOMETHING I WROTE.

THANKS,
DEAN

"""

MoveStruct = namedtuple("MoveStruct", "moveType i j")

class MoveType:
    Take = "itmightbemorefunifthesethingsarejustrandomstringslul"
    Defend = 2
    Prepare = 3

class Mark:
    Empty = "."
    X = "X" # made these strings for ease of printing
    O = "O"

moveTypes = (MoveType.Take, MoveType.Defend, MoveType.Prepare)
markTypes = (Mark.Empty, Mark.X, Mark.O)

def whatiserrorhandling():
    raise Exception("something went horribly wrong and I'm too lazy to tell you what")

def opposite(mark):
    assert mark == Mark.X or mark == Mark.O
    if mark == Mark.X:
        return Mark.O
    elif mark == Mark.O:
        return Mark.X
    else:
        whatiserrorhandling()

class Player():
    def __init__(self, name="defaultname"):
        self.name = name
        self.prepped = False
        self.mark = Mark.Empty

    def get_move(self, board, blocks):
        legalMoves = self.get_legal_moves(board, blocks)
        return random.choice(legalMoves)
    
    def get_legal_moves(self, board, blocks):
        legalCoords = self.get_legal_coords(board, blocks)
        legalMoves = []
        legalMoves.append(MoveStruct(MoveType.Prepare, 0, 0))
        for coord in legalCoords:
            for move in (MoveType.Take, MoveType.Defend):
                move = MoveStruct(move, coord[0], coord[1])
                legalMoves.append(move)
        return legalMoves

    def get_legal_coords(self, board, blocks):
        legalCoords = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != Mark.Empty:
                    pass
                elif blocks[i][j] >= 1:
                    # If it's a win move, it's legal (is it legal for block and take or just take? I know it doesn't matter, but it kinda matters)
                    # Block doesn't select a coordinate, right? If it was previously blocked, I think it's illegal until unblocked even if it would win the game
                    if themovewouldwinthegamesrayoudothisimlazy(board, self.mark):
                        legalCoords.append((i, j))
                    else:
                        pass
                # If it's empty and it's not blocked it's legal
                else:
                    legalCoords.append((i, j))
        return legalCoords


def themovewouldwinthegamesrayoudothisimlazy(board, mark):
    # TODO
    # check row
    # check column
    # check NW->SE diagonal
    # check SW->NE diagonal

    return False

class GameInstance():
    GAMEBOARDSIZE = 3
    BLOCKDURATION = 2
    WINCONLENGTH = 3

    # @@@ maybe we want to add a sanity check for winconlength <= gameboardsize

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.winner = None
        self.board = [[Mark.Empty for i in range(self.GAMEBOARDSIZE)] for j in range(self.GAMEBOARDSIZE)]
        # Sarah: i changed this line
        # Dean: you forgot to change the two lines below this, they had the same problem. I changed them
        self.p1blocked = [[0 for i in range(self.GAMEBOARDSIZE)] for j in range(self.GAMEBOARDSIZE)]
        self.p2blocked = [[0 for i in range(self.GAMEBOARDSIZE)] for j in range(self.GAMEBOARDSIZE)]
        self.assign_marks()

    def assign_marks(self):
        self.p1.mark = Mark.X
        self.p2.mark = Mark.O

    def validate_coord(self, i, j):
        assert i >= 0 and i < self.GAMEBOARDSIZE
        assert j  >= 0 and j  < self.GAMEBOARDSIZE

    def apply_move(self, move, player):
        # Dean: this should be basically done
        assert type(move) == MoveStruct
        # Prepare
        if move.moveType == MoveType.Prepare:
            player.prepped = True 
        # Defend
        #TODO this was done assuming block requires a coordinate
        elif move.moveType == MoveType.Defend:       
            if player == self.p1:
                self.p1defend(move.i, move.j)
            elif player == self.p2:
                self.p2defend(move.i, move.j)
        # Take
        elif move.moveType == MoveType.Take:       
            self.mark_board(move.i, move.j, player.mark)
        else:
            whatiserrorhandling()

    def mark_board(self, i, j, mark):
        self.validate_coord(i, j)
        assert self.board[i][j] == Mark.Empty
        assert mark in markTypes
        # @@@ assert type(mark) == Mark is wrong. Mark.X is an int
        assert mark != Mark.Empty
        self.board[i][j] = mark

    def p1defend(self, i, j):
        #TODO this was done assuming block requires a coordinate
        self.validate_coord(i,j)
        self.p2blocked[i][j] = self.BLOCKDURATION

    def p2defend(self, i, j):
        #TODO this was done assuming block requires a coordinate
        self.validate_coord(i, j)
        self.p1blocked[i][j] = self.BLOCKDURATION

    def gameloop(self):
        # TODO this ain't done
        # Dean: I changed this to use my apply_move function 
        # Dean: This function assumes that it doesn't receive illegal moves. Therefore it doesn't check if spaces are blocked from previous turns
        #       not sure if this is the right functionality, can change later if need be. 
        while not self.winner:
            p1move = self.p1.get_move(self.board, self.p1blocked)
            p2move = self.p2.get_move(self.board, self.p2blocked)
            # if either player chooses to prepare, both moves go off
            if p1move.moveType == MoveType.Prepare or p2move.moveType == MoveType.Prepare:
                self.apply_move(p1move, self.p1)
                self.apply_move(p2move, self.p2)
            elif p1move.i == p2move.i and p1move.j == p2move.j:
                # @@@ TODO
                # special interactions only happen when you try to go to the same spot
                # exception: prep-take on a spot that was defended the previous turn (handle this while checking if a move is legal)
                # is this correct?: a prepped move will always beat out a non-prepped move on the same square
                if self.p1.prepped and not self.p2.prepped:
                    self.apply_move(p1move, self.p1)
                elif self.p2.prepped and not self.p1.prepped:
                    self.apply_move(p2move, self.p2)
                # is this correct?: interactions are identical if both moves are prepped or both moves are unprepped
                elif p1move.moveType == p2move.moveType:
                    # is this correct?: if both people block the same square they both fail
                    pass
                elif p1move.moveType == MoveType.Defend and p2move.moveType == MoveType.Take:
                    self.apply_move(p1move, self.p1)
                elif p2move.moveType == MoveType.Defend and p1move.moveType == MoveType.Take:
                    self.apply_move(p2move, self.p2)
            else:
                self.apply_move(p1move, self.p1)
                self.apply_move(p2move, self.p2)
            self.check_for_winner()

    def pretty_print(self):
        s = "\n"
        for i in range(self.GAMEBOARDSIZE): 
            s += "\t" + "     |"*self.GAMEBOARDSIZE + "\b \n\t"
            for j in range(self.GAMEBOARDSIZE):
                s += "  {}  |".format(self.board[i][j])
            if i == self.GAMEBOARDSIZE - 1:
                s += "\b \n\t" + "     |"*self.GAMEBOARDSIZE + "\b \n"
            else:
                s += "\b \n\t" + "_____|"*self.GAMEBOARDSIZE + "\b \n"
        s += "\r"
        s += " "*self.GAMEBOARDSIZE*7
        print(s)

    def check_for_winner(self):
        # Dean: I didn't touch this
        # set self.winner to p1 or p2 if there's a winner
        # ok this is really ugly but whatever

        x_count = 0
        o_count = 0
        # check rows
        for i in range(0, self.GAMEBOARDSIZE):
            for j in range(0, self.GAMEBOARDSIZE):
                if self.board[i][j] == Mark.X:
                    x_count += 1
                    o_count = 0
                elif self.board[i][j] == Mark.O:
                    x_count = 0
                    o_count += 1
                else:
                    x_count = 0
                    o_count = 0
                if x_count >= self.WINCONLENGTH:
                    self.winner = self.p1
                    return
                if o_count >= self.WINCONLENGTH:
                    self.winner = self.p2
                    return
        
        # check columns
        for j in range(0, self.GAMEBOARDSIZE):
            for i in range(0, self.GAMEBOARDSIZE):
                if self.board[i][j] == Mark.X:
                    x_count += 1
                    o_count = 0
                elif self.board[i][j] == Mark.O:
                    x_count = 0
                    o_count += 1
                else:
                    x_count = 0
                    o_count = 0
                if x_count >= self.WINCONLENGTH:
                    self.winner = self.p1
                    return
                if o_count >= self.WINCONLENGTH:
                    self.winner = self.p2
                    return
              
        # check NW->SE diagonals
        for i in range(0, self.GAMEBOARDSIZE-self.WINCONLENGTH+1):
            for j in range(0, self.GAMEBOARDSIZE-i):
                if self.board[i+j][j] == Mark.X:
                    x_count += 1
                    o_count = 0
                elif self.board[i+j][j] == Mark.O:
                    x_count = 0
                    o_count += 1
                else:
                    x_count = 0
                    o_count = 0
                if x_count >= self.WINCONLENGTH:
                    self.winner = self.p1
                    return
                if o_count >= self.WINCONLENGTH:
                    self.winner = self.p2
                    return
        for j in range(1, self.GAMEBOARDSIZE-self.WINCONLENGTH+1):
            for i in range(0, self.GAMEBOARDSIZE-j):
                if self.board[i][j+i] == Mark.X:
                    x_count += 1
                    o_count = 0
                elif self.board[i][j+i] == Mark.O:
                    x_count = 0
                    o_count += 1
                else:
                    x_count = 0
                    o_count = 0
                if x_count >= self.WINCONLENGTH:
                    self.winner = self.p1
                    return
                if o_count >= self.WINCONLENGTH:
                    self.winner = self.p2
                    return
                    
        # check SW->NE diagonals
        for i in range(self.WINCONLENGTH-1, self.GAMEBOARDSIZE):
            for j in range(0, i+1):
                if self.board[i-j][j] == Mark.X:
                    x_count += 1
                    o_count = 0
                elif self.board[i-j][j] == Mark.O:
                    x_count = 0
                    o_count += 1
                else:
                    x_count = 0
                    o_count = 0
                if x_count >= self.WINCONLENGTH:
                    self.winner = self.p1
                    return
                if o_count >= self.WINCONLENGTH:
                    self.winner = self.p2
                    return
        for j in range(1, self.GAMEBOARDSIZE-self.WINCONLENGTH+1):
            for i in range(0, self.GAMEBOARDSIZE-j):
                if self.board[i][j+i] == Mark.X:
                    x_count += 1
                    o_count = 0
                elif self.board[i][j+i] == Mark.O:
                    x_count = 0
                    o_count += 1
                else:
                    x_count = 0
                    o_count = 0
                if x_count >= self.WINCONLENGTH:
                    self.winner = self.p1
                    return
                if o_count >= self.WINCONLENGTH:
                    self.winner = self.p2
                    return
        # no winner found
        return


