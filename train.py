from board import *

def match(champ, rookie):
    log = {}
    log["move_count"] = 0
    log["repeat_count"] = 0
    log["winning_network"] = "champ"

    print "starting match"
    board = Board()
    #champ = Network([128, 40, 1])
    # rookie = champ.get_copy()
    # rookie.perturb()

    if random.random() < 0.5:
        green_network = rookie
        red_network = champ
    else:
        green_network = champ
        red_network = rookie

    curr_player = G

    move_count = 0
    visited_states = {}
    while True:
        #print "%s's turn" % ali_name(curr_player)
        #print board
        eps = 0.05
        if str(board) in visited_states and visited_states[str(board)] > 3:
            eps = 1 - (1 / visited_states[str(board)])
            log["repeat_count"] += 1
        if curr_player == G:
            move = board.get_move_from_network(green_network, G, eps)
        elif curr_player == R:
            move = board.get_move_from_network(red_network, R, eps)
        #print move
        if move is None:
            print move_count
            #print "Game over, %s loses" % ali_name(curr_player)
            if curr_player == R:
                log["winner"] = "red"
            else:
                log["winner"] = "green"
            if (curr_player == R and green_network == rookie) or (curr_player == G and red_network == rookie): # red lost and green was using the rookie network
                log["winning_network"] = "rookie"
                #print "Rookie wins!"
                #champ.weighted_average(rookie, 0.7)
            break
        else:
            move_count += 1
            log["move_count"] += 1
            for atomic_move in move:
                atomic_move.make()
            if str(board) in visited_states:
                visited_states[str(board)] += 1
            else:
                visited_states[str(board)] = 1
            if curr_player == G:
                curr_player = R
            elif curr_player == R:
                curr_player = G
        if move_count > 200:
            print move_count
            red_count = board.get_piece_count(R)
            green_count = board.get_piece_count(G)
            if green_count > red_count:
                print "Green wins by draw"
                log["winner"] = "green"
                if green_network == rookie:
                    log["winning_network"] = "rookie"
            elif red_count > green_count:
                print "Red wins by draw"
                log["winner"] = "red"
                if red_network == rookie:
                    log["winning_network"] = "rookie"
            else:
                print "G %i || R %i" % (green_count, red_count)
                log["winner"] = "draw"
            log["note"] = "technical draw"
            break

    return log

def train(match_num):
    champ = Network([512, 10, 10, 1])
    round_num = 0
    total_rookie_wins = 0
    while(round_num < 5000):
        rookie = champ.get_copy()
        rookie.perturb()
        rookie_win_count = 0
        print "Round %i" % (round_num + 1)
        for i in range(1, 5):
            log = match(champ, rookie)
            f = open("log/%i_%i.txt" % (round_num, i), "wb+")
            f.write(str(log))
            f.close()
            if log["winning_network"] == "rookie":
                rookie_win_count += 1
            print "Rookie: %i / %i" % (rookie_win_count, i)
            if rookie_win_count == 3:
                total_rookie_wins += 1
                print "ROOKIE WINS! (%i)" % total_rookie_wins
                champ.weighted_average(rookie, 0.8)
                break
            if (4 - i) + rookie_win_count < 3: # rookie can't win
                break
        champ.serialize("round_%i" % round_num)
        round_num += 1
        print "\n"
    return curr_network

def ali_name(alliance):
    if alliance == G:
        return "Green"
    else:
        return "Red"

train(20000)
