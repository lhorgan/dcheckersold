from constants import *

class AtomicMove:
    def __init__(self, board, checker, start, end, victim=None):
        self.board = board
        self.checker = checker
        self.start = (checker.row, checker.col)
        self.is_king_at_start = self.checker.is_king
        self.end = end
        self.victim = victim

    def make(self):
        self.board.set_checker(self.start, None)
        self.board.set_checker(self.end, self.checker)
        self.checker.set_pos(self.end)
        if self.checker.alliance == G and self.end[0] == 7 or \
        self.checker.alliance == R and self.end[0] == 0:
            self.checker.is_king = True
        if self.victim is not None:
            self.board.set_checker(self.victim.get_pos(), None)

    def undo(self):
        self.board.set_checker(self.start, self.checker)
        self.checker.set_pos(self.start)
        self.checker.is_king = self.is_king_at_start
        self.board.set_checker(self.end, None)
        if self.victim is not None:
            self.board.set_checker(self.victim.get_pos(), self.victim)

    def __str__(self):
        return "%s --> %s" % (self.start, self.end)

    def __repr__(self):
        return self.__str__()
