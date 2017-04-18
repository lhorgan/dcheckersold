import pygame
from board import *
from constants import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SIZE = 512
INC = int(SIZE / 8)

def game_loop():
    pygame.init()

    size = (SIZE, SIZE)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Checkers")
    game_over = False
    clock = pygame.time.Clock()
    board = Board()

    screen.fill(WHITE)
    render_board(board, screen)
    pygame.display.flip()
    selected_checker = None

    network = Network([])
    print "loading 513"
    network.load("round_4950")

    human = R
    computer = G
    curr_player = R

    if curr_player == computer:
        screen.fill(WHITE)
        computer_move(board, network, computer)
        render_board(board, screen)
        curr_player = human
        pygame.display.flip()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONUP and curr_player == human:
                pos = pygame.mouse.get_pos()
                if board.get_checker(resolve_checker(pos)) is not None:
                    selected_checker = resolve_checker(pos)
                    print board.get_checker(resolve_checker(pos)).get_legal_moves()
                    #attacked_by_red = board.attacking(R)
                    #attacked_by_green = board.attacking(G)
                    #print board.encode_space(selected_checker[0], selected_checker[1], attacked_by_green, attacked_by_red)
                    #print board.get_network_encoding()
                    screen.fill(WHITE)
                    render_board(board, screen)
                    highlight_legal(board, resolve_checker(pos), screen)
                    pygame.display.flip()
                else:
                    screen.fill(WHITE)
                    if selected_checker is not None:
                        selected_endpoint = resolve_checker(pos)
                        res = attempt_move(board, selected_checker, selected_endpoint)
                        selected_checker = None
                        if res == True:
                            curr_player = computer
                            computer_move(board, network, computer)
                            curr_player = human
                    render_board(board, screen)
                    pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def cage_match():
    network_green = Network([])
    network_green.load("round_27225")
    network_red = Network([])
    network_red.load("round_27225")

    curr_player = G
    board = Board()

    size = (SIZE, SIZE)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Checkers")
    clock = pygame.time.Clock()

    screen.fill(WHITE)
    render_board(board, screen)
    pygame.display.flip()

    import time
    move_status = True
    while True:
        print curr_player
        if move_status:
            if curr_player == G:
                move_status = computer_move(board, network_green, curr_player, True)
            elif curr_player == R:
                move_status = computer_move(board, network_red, curr_player)
        screen.fill(WHITE)
        render_board(board, screen)
        pygame.display.flip()
        #clock.tick(10000000)
        #time.sleep(0.1)
        curr_player = get_other_player(curr_player)

def computer_move(board, network, computer, random_play=False):
    if random_play:
        moves = board.get_legal_moves(computer)
        print "legal moves are"
        print moves
        if len(moves) == 0:
            return False
        move_seq = random.choice(moves)
    else:
        move_seq = board.get_best_move_ab(2, computer, network)
        #move_seq = board.get_move_from_network(network, computer)
        print "SELECTING"
        if move_seq is None:
            print "\nI have no legal moves\n"
            return False
        print move_seq
    for atomic_move in move_seq:
        atomic_move.make()
    return True

def get_other_player(curr_player):
    if curr_player == G:
        return R
    else:
        return G

def attempt_move(board, selected_checker, selected_endpoint):
    checker = board.get_checker(selected_checker)
    if checker is not None:
        legal = checker.get_legal_moves()
        for move_seq in legal:
            last_move = move_seq[-1]
            if last_move.end == selected_endpoint:
                for atomic_move in move_seq:
                    atomic_move.make()
                return True
    return False

def resolve_checker(click_pos):
    x, y = click_pos
    row = int((y / float(SIZE)) * 8)
    col = int((x / float(SIZE)) * 8)
    return (row, col)

def highlight_legal(board, pos, screen):
    checker = board.get_checker(pos)
    if checker is not None:
        legal = checker.get_legal_moves()
        for move_seq in legal:
            last_move = move_seq[-1]
            to_highlight = last_move
            last_moveX = last_move.end[1] * INC
            last_moveY = last_move.end[0] * INC
            off = INC / 8
            pygame.draw.ellipse(screen, BLUE, [last_moveX + off / 2, last_moveY + off / 2, INC - off, INC - off], 3)

def render_board(board, screen):
    posY = 0
    for i in range(0, 8):
        posX = 0
        for j in range(0, 8):
            checker = board.get_checker((i, j))
            if i % 2 == 0:
                if j % 2 == 0:
                    color = WHITE
                else:
                    color = BLACK
            else:
                if j % 2 == 0:
                    color = BLACK
                else:
                    color = WHITE
            pygame.draw.rect(screen, color, [posX, posY, INC, INC])
            if checker is not None:
                off = INC / 8
                if checker.alliance == G:
                    checker_color = GREEN
                elif checker.alliance == R:
                    checker_color = RED
                pygame.draw.ellipse(screen, checker_color, [posX + off / 2, posY + off / 2, INC - off, INC - off])
            posX += INC
        posY += INC

#game_loop()
cage_match()
