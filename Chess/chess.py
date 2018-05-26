from time import sleep
from random import random

class Chess_Board():
    def __init__(self):
        self.width = self.height = 8
        self.w = {(7,0):'r', (7,7):'r', (7,1):'n', (7,6):'n',\
                  (7,2):'b', (7,5):'b', (7,3):'q', (7,4):'k',\
                  (6,0):'p', (6,1):'p', (6,2):'p', (6,3):'p',\
                  (6,4):'p', (6,5):'p', (6,6):'p', (6,7):'p'}
        self.b = {(0,0):'r', (0,7):'r', (0,1):'n', (0,6):'n',\
                  (0,2):'b', (0,5):'b', (0,3):'q', (0,4):'k',\
                  (1,0):'p', (1,1):'p', (1,2):'p', (1,3):'p',\
                  (1,4):'p', (1,5):'p', (1,6):'p', (1,7):'p'}

    """
    Black pieces are in upper-letters
    White pieces are in lower-letters
    N represents a knight
    K represents a king
    """
    def __str__(self):
        rtn_str = ''
        board =    '\n'
        board += '  -------b-------\n'
        board += '  0 1 2 3 4 5 6 7\n'
        bs = self.b.keys()
        ws = self.w.keys()

        for i in range(self.height):
            board += str(i) + ' '
            for j in range(self.width):
                if (i, j) in bs:
                    board += self.b[(i,j)]
                elif (i, j) in ws:
                    board += self.w[(i,j)].upper()
                else:
                    board += '_'
                board += ' '

            board += '\n'
        board += '  -------W-------\n\n'
        rtn_str += board
        rtn_str += 'Number of black alive: ' + str(len(self.b)) + '\n'
        rtn_str += 'Number of white alive: ' + str(len(self.w)) + '\n'

        return rtn_str

    def out_of_boundary(self, pos):
        if pos[0] >= 0 and pos[0] < self.height and \
           pos[1] >= 0 and pos[1] < self.width:
            return False

        return True

    # We don't need to worry about when pawn hits the boundary since they turn into
    # Queen once they hit the other end
    def get_pawn_moves(self, player, pos):
        possible_moves = []

        if player == 'b':
            if (pos[0]+1, pos[1]) not in self.b.keys() + self.w.keys():
                possible_moves.append((pos[0]+1, pos[1]))

            if (pos[0]+1, pos[1]+1) in self.w.keys():
                possible_moves.append((pos[0]+1, pos[1]+1))

            if (pos[0]+1, pos[1]-1) in self.w.keys():
                possible_moves.append((pos[0]+1, pos[1]-1))
        elif player == 'w':
            if (pos[0]-1, pos[1]) not in self.b.keys() + self.w.keys():
                possible_moves.append((pos[0]-1, pos[1]))

            if (pos[0]-1, pos[1]+1) in self.b.keys():
                possible_moves.append((pos[0]-1, pos[1]+1))

            if (pos[0]-1, pos[1]-1) in self.b.keys():
                possible_moves.append((pos[0]-1, pos[1]-1))

        return possible_moves

    def get_rook_moves(self, player, pos):
        possible_moves = []

        if player == 'b':
            ally = self.b.keys()
            opponent = self.w.keys()
        elif player == 'w':
            ally = self.w.keys()
            opponent = self.b.keys()
 
        # Going up
        for i in range(pos[0]-1, -1, -1):
            if (i, pos[1]) in opponent:
                possible_moves.append((i, pos[1]))
                break
            elif (i, pos[1]) not in ally:
                possible_moves.append((i, pos[1]))
            else: # position is in ally
                break
        # Going down
        for i in range(pos[0]+1, self.height):
            if (i, pos[1]) in opponent:
                possible_moves.append((i, pos[1]))
                break
            elif (i, pos[1]) not in ally:
                possible_moves.append((i, pos[1]))
            else: # position is in ally
                break
        # Going right
        for i in range(pos[1]+1, self.width):
            if (pos[0], i) in opponent:
                possible_moves.append((pos[0], i))
                break
            elif (pos[0], i) not in ally:
                possible_moves.append((pos[0], i))
            else: # position is in ally
                break
        # Going left
        for i in range(pos[1]-1, -1, -1):
            if (pos[0], i) in opponent:
                possible_moves.append((pos[0], i))
                break
            elif (pos[0], i) not in ally:
                possible_moves.append((pos[0], i))
            else: # position is in ally
                break

        return possible_moves

    def get_king_moves(self, player, pos):
        possible_moves =[(pos[0], pos[1]+1),(pos[0], pos[1]-1),
                         (pos[0]+1, pos[1]),(pos[0]+1, pos[1]+1),(pos[0]+1, pos[1]-1),\
                         (pos[0]-1, pos[1]),(pos[0]-1, pos[1]+1),(pos[0]-1, pos[1]-1)]

        if player == 'b':
            ally = self.b.keys()
        else:
            ally = self.w.keys()

        i = 0
        while i < len(possible_moves):
            if possible_moves[i] in ally:
                possible_moves.pop(i)
            elif self.out_of_boundary(possible_moves[i]):
                possible_moves.pop(i)
            else:
                i += 1

        return possible_moves

    def get_knight_moves(self, player, pos):
        possible_moves = [(pos[0]+2,pos[1]+1),(pos[0]+2,pos[1]-1),\
                          (pos[0]-2,pos[1]+1),(pos[0]-2,pos[1]+1),\
                          (pos[0]+1,pos[1]+2),(pos[0]-1,pos[1]+2),\
                          (pos[0]+1,pos[1]-2),(pos[0]-1,pos[1]-2),]

        if player == 'b':
            ally = self.b.keys()
        else:
            ally = self.w.keys()

        i = 0
        while i < len(possible_moves):
            if possible_moves[i] in ally:
                possible_moves.pop(i)
            elif self.out_of_boundary(possible_moves[i]):
                possible_moves.pop(i)
            else:
                i += 1

        return possible_moves

    def get_bishop_moves(self, player, pos):
        possible_moves = []

        if player == 'b':
            ally = self.b.keys()
            opponent = self.w.keys()
        elif player == 'w':
            ally = self.w.keys()
            opponent = self.b.keys()

        # Going up right
        r,c = pos
        while not self.out_of_boundary((r,c)):
            if (r,c) in opponent:
                possible_moves.append((r,c))
                break
            elif (r,c) not in ally:
                possible_moves.append((r,c))
            else:
                break
            r -= 1
            c += 1
        # Going up left
        r,c = pos
        while not self.out_of_boundary((r,c)):
            if (r,c) in opponent:
                possible_moves.append((r,c))
                break
            elif (r,c) not in ally:
                possible_moves.append((r,c))
            else:
                break
            r -= 1
            c -= 1
        # Going down right
        r,c = pos
        while not self.out_of_boundary((r,c)):
            if (r,c) in opponent:
                possible_moves.append((r,c))
                break
            elif (r,c) not in ally:
                possible_moves.append((r,c))
            else:
                break
            r += 1
            c += 1
        # Going down left
        r,c = pos
        while not self.out_of_boundary((r,c)):
            if (r,c) in opponent:
                possible_moves.append((r,c))
                break
            elif (r,c) not in ally:
                possible_moves.append((r,c))
            else:
                break
            r += 1
            c -= 1

        return possible_moves

    def get_queen_moves(self, player, pos):
        possible_moves = self.get_bishop_moves(player, pos) +\
                         self.get_rook_moves(player, pos)
        return possible_moves

    def can_move(self, player, piece, pos):
        possible_moves = []

        if piece == 'p':
            possible_moves = self.get_pawn_moves(player, pos)
        elif piece == 'r':
            possible_moves = self.get_rook_moves(player, pos)
        elif piece == 'k':
            possible_moves = self.get_king_moves(player, pos)
        elif piece == 'n':
            possible_moves = self.get_knight_moves(player, pos)
        elif piece == 'b':
            possible_moves = self.get_bishop_moves(player, pos)
        elif piece == 'q':
            possible_moves = self.get_queen_moves(player, pos)

        print('original position: ', pos)
        print('possible moves: ', possible_moves)

        if len(possible_moves) > 0:
            return True, possible_moves
        elif len(possible_moves) == 0:
            return False, None

    def check_moves(self, player):
        if player == 'b':
            for pos in self.b:
                if self.can_move('b', self.b[pos], pos)[0]:
                    return True
        elif player == 'w':
            for pos in self.w:
                if self.can_move('w', self.w[pos], pos)[0]:
                    return True

        return False
    
    def is_game_over(self):
        # When a king was captured
        if 'k' not in self.b.values() or 'k' not in self.w.values():
            return True
        # When there is no available moves from either side
        elif self.check_moves('b') == False and self.check_moves('w') == False:
            return True

        return False

    def move(self, player, orig_pos, dest_pos):
        if player == 'b':
            p_pieces = self.b
            o_pieces = self.w
        elif player == 'w':
            p_pieces = self.w
            o_pieces = self.b

        piece = p_pieces.pop(orig_pos)

        # Remove an opponent's piece
        if dest_pos in o_pieces.keys():
            o_pieces.pop(dest_pos)

        # New position
        p_pieces[dest_pos] = piece

    def auto_random(self):
        print(self)
        print("Auto game started!")
        print("Random mode!")
        print('')
        curr_player = 'w'
        sleep(3)

        while self.is_game_over() != True:
            if curr_player == 'w':
                print("White's turn")
                pieces = self.w
            elif curr_player == 'b':
                print("Black's turn")
                pieces = self.b

            options = set(pieces.values())
            pieces = int(random() * (len(options)+1))


    def start_game(self):
        print(self)
        print("Game started!")
        print('')
        # Start with white
        curr_player = 'w'

        ############ MAIN LOOP ###############
        ######################################
        while self.is_game_over() != True:
            if curr_player == 'w':
                print("White's turn")
                pieces = self.w
            elif curr_player == 'b':
                print("Black's turn")
                pieces = self.b

            ############ Choosing Piece ###############
            ###########################################
            print('')
            print("Choose a piece to move")
            options = set(pieces.values())
            print("Options: " + str(set(pieces.values()))[4:-1])
            piece = raw_input(':')
            # Catching not available piece entry
            while piece not in options:
                print("Invalid entry")
                print('')
                print("Choose a piece to move")
                print("Options: " + str(set(pieces.values()))[4:-1])
                piece = raw_input(':')
            print('')

            ############ Which One ###############
            ######################################
            options = [x for x in pieces if pieces[x] == piece]
            # Choose from multiple options
            if len(options) > 1:
                print("Which one?")
                print("Options: " + str(options))
                orig_pos_raw = raw_input(':').replace('(','').replace(')','').replace(',','')
                orig_pos = (int(orig_pos_raw[0]),int(orig_pos_raw[1]))
                # Catching not available position entry
                while orig_pos not in options:
                    print("Invalid entry")
                    print('')
                    print("Which one?")
                    print("Options: " + str(options))
                    orig_pos_raw = raw_input(':').replace('(','').replace(')','').replace(',','')
                    orig_pos = (int(orig_pos_raw[0]),int(orig_pos_raw[1]))
            # Only one option available
            elif len(options) == 1:
                orig_pos = options[0]
            print('')

            ############ Where to ###############
            #####################################
            print("Where to?")
            options = self.can_move(curr_player, piece, orig_pos)[1]
            print("options: " + str(options))
            new_pos_raw = raw_input(':').replace('(','').replace(')','').replace(',','')
            new_pos = (int(new_pos_raw[0]), int(new_pos_raw[1]))
            # Catching not available position entry
            while new_pos not in options:
                print("Invalid entry")
                print('')
                print("Where to?")
                print("options: " + self.can_move(curr_player, piece, orig_pos)[1])
                new_pos_raw = raw_input(':').replace('(','').replace(')','').replace(',','')
                new_pos = (int(new_pos_raw[0]), int(new_pos_raw[1]))

            self.move(curr_player, orig_pos, new_pos)
            print(self)

            if curr_player == 'w':
                curr_player = 'b'
            elif curr_player == 'b':
                curr_player = 'w'

b=Chess_Board()
b.start_game()
