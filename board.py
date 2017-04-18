from checker import *

class Board:
    def __init__(self):
        self.state = [None] * 8
        for i in range(0, 8):
            self.state[i] = [None] * 8

        starting_config = [
            [0, g, 0, g, 0, g, 0, g],
            [g, 0, g, 0, g, 0, g, 0],
            [0, g, 0, g, 0, g, 0, g],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [r, 0, r, 0, r, 0, r, 0],
            [0, r, 0, r, 0, r, 0, r],
            [r, 0, r, 0, r, 0, r, 0]
        ]
        self.set_state(starting_config)

    def set_state(self, config):
        for i in range(0, 8):
            for j in range(0, 8):
                if config[i][j] > 0:
                    alliance = G if config[i][j] == g or config[i][j] == G else R
                    is_king = config[i][j] == G or config[i][j] == R
                    self.state[i][j] = Checker(self, alliance, is_king, i, j)
                else:
                    self.state[i][j] = None

    def get_checker(self, pos):
        if not self.on_board(pos):
            return -1
        row, col = pos
        return self.state[row][col]

    def set_checker(self, pos, checker):
        row, col = pos
        self.state[row][col] = checker

    def on_board(self, pos):
        row, col = pos
        return (0 <= row < 8) and (0 <= col < 8)

    def get_network_encoding(self):
        red_arr = []
        green_arr = []
        attacked_by_green = self.attacking(G)
        attacked_by_red = self.attacking(R)
        for i in range(0, 8):
            for j in range(0, 8):
                if self.state[i][j] is None:
                    red_arr += [0.0, 0.0, 0.0, 0.0]
                    green_arr += [0.0, 0.0, 0.0, 0.0]
                elif self.state[i][j].alliance == R:
                    red_arr += self.encode_space(i, j, attacked_by_green, attacked_by_red)
                    green_arr += [0.0, 0.0, 0.0, 0.0]
                elif self.state[i][j].alliance == G:
                    red_arr += [0.0, 0.0, 0.0, 0.0]
                    green_arr += self.encode_space(i, j, attacked_by_green, attacked_by_red)
        return green_arr + red_arr

    def encode_space(self, row, col, attacked_by_green, attacked_by_red):
        encoding = [0.0, 0.0, 0.0, 0.0]
        checker = self.state[row][col]
        if checker is not None:
            encoding[0] = 1.0
            # the checker is safe
            if checker.alliance == R and checker not in attacked_by_green:
                #print "I'm red and safe"
                encoding[1] = 1.0
            elif checker.alliance == G and checker not in attacked_by_red:
                #print "I'm green and safe"
                encoding[1] = 1.0
            else:
                #print "I'm not safe!"
                pass
            if checker.is_defended():
                #print "I'm defended"
                encoding[2] = 1.0
            if checker.is_king:
                #print "I'm a king"
                encoding[3] = 1.0
        return encoding

    def count_kings(self, alliance):
        king_num
        for i in range(0, 8):
            for j in range(0, 8):
                checker = self.state[i][j]
                if checker is not None and checker.alliance == alliance:
                    king_num += 1
        return king_num

    def attacking(self, alliance):
        attacked = set()
        legal_moves = self.get_legal_moves(alliance)
        for move_seq in legal_moves:
            for atomic_move in move_seq:
                if atomic_move.victim is not None:
                    attacked.add(atomic_move.victim)
        return attacked

    def get_enemy(self, alliance):
        if alliance == G:
            return R
        else:
            return G

    def get_legal_moves(self, alliance):
        legal_moves = []
        for i in range(0, 8):
            for j in range(0, 8):
                checker = self.state[i][j]
                if checker is not None and checker.alliance == alliance:
                    legal_moves += checker.get_legal_moves()
        return legal_moves

    # adapted from Wikipedia pseudo-code
    def ab_prune(self, depth, player, network, a=-float("inf"), b=float("inf")):
        legal_moves = self.get_legal_moves(player)
        if depth == 0 or len(legal_moves) == 0:
            network.set_input(self.get_network_encoding())
            output = network.get_output()[0]
            #print "OUTPUT: %d" % output
            return output
        if player == G: # max agent
            value = -float("inf")
            for move_seq in legal_moves:
                for atomic_move in move_seq:
                    atomic_move.make()
                value = max(value, self.ab_prune(depth - 1, R, network, a, b))
                for i in range(len(move_seq) - 1, -1, -1):
                    move_seq[i].undo()
                a = max(a, value)
                if b <= a:
                    break
            return value
        else:
            value = float("inf")
            for move_seq in legal_moves:
                for atomic_move in move_seq:
                    atomic_move.make()
                value = min(value, self.ab_prune(depth - 1, G, network, a, b))
                for i in range(len(move_seq) - 1, -1, -1):
                    move_seq[i].undo()
                b = min(b, value)
                if b <= a:
                    break
            return value

    def get_best_move_ab(self, depth, player, network):
        legal_moves = self.get_legal_moves(player)
        best_move = None
        if player == G:
            best_move_val = -float("inf")
        else:
            best_move_val = float("inf")
        for move_seq in legal_moves:
            for atomic_move in move_seq:
                atomic_move.make()
            network.set_input(self.get_network_encoding())
            #value = network.get_output()[0]
            value = self.ab_prune(depth - 1, self.get_enemy(player), network)
            print "VALUE: %s" % value
            if player == G and value >= best_move_val:
                best_move_val = value
                best_move = move_seq
            elif player == R and value <= best_move_val:
                best_move_val = value
                best_move = move_seq
            for i in range(len(move_seq) - 1, -1, -1):
                move_seq[i].undo()
        return best_move

    def get_piece_count(self, alliance):
        count = 0
        #print(self.__str__())
        for i in range(0, 8):
            for j in range(0, 8):
                checker = self.state[i][j]
                if checker is not None and checker.alliance == alliance:
                    #print "COOL"
                    count += 1
        return count

    def get_move_from_network(self, network, alliance, eps=0.05):
        legal_moves = self.get_legal_moves(alliance)
        #print "ALL LEGAL MOVES"
        #print legal_moves
        if len(legal_moves) > 0:
            if random.random() < eps:
                return random.choice(legal_moves)
            else:
                if alliance == G:
                    best_output = -float("inf")
                elif alliance == R:
                    #print "tis el turn de red"
                    best_output = float("inf")
                best_move = None
                for move_seq in legal_moves:
                    #print "dope"
                    for i in range(0, len(move_seq)):
                        move_seq[i].make()
                    network.set_input(self.get_network_encoding())
                    output = network.get_output()
                    #print output
                    output = output[0]
                    if (output >= best_output and alliance == G) or (output <= best_output and alliance == R):
                        #print "sick bro"
                        best_output = output
                        best_move = move_seq
                    for i in range(len(move_seq) - 1, -1, -1):
                        move_seq[i].undo()
                return best_move
        else:
            return None

    def __str__(self):
        str = ""
        for i in range(0, 8):
            for j in range(0, 8):
                checker = self.state[i][j]
                if checker is not None:
                    if checker.alliance == G:
                        if checker.is_king:
                            str += " G "
                        else:
                            str += " g "
                    elif checker.alliance == R:
                        if checker.is_king:
                            str += " R "
                        else:
                            str += " r "
                else:
                    str += " - "
            str += "\n"
        return str
