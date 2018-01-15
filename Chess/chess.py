from time import sleep
from random import random

class Chess_Board():
  def __init__(self):
    self.width = self.height = 8
    self.w = {(7,0):'l', (7,7):'l', (7,1):'n', (7,6):'n',\
              (7,2):'b', (7,5):'b', (7,3):'q', (7,4):'k',\
              (6,0):'p', (6,1):'p', (6,2):'p', (6,3):'p',\
              (6,4):'p', (6,5):'p', (6,6):'p', (6,7):'p'}
    self.b = {(0,0):'l', (0,7):'l', (0,1):'n', (0,6):'n',\
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
    board =  '\n'
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

  def is_valid_move(self, player, orig_pos, dest_pos):
    # Invalid position check
    if orig_pos[0] < 0 or orig_pos[1] < 0 or dest_pos[0] < 0 or dest_pos[1] < 0 or \
      orig_pos[0] > 7 or orig_pos[1] > 7 or dest_pos[0] > 7 or dest_pos[1] > 7:
      return False

    # Check validity of the given orig_pos and piece
    # Black
    if player == 'b':
      if orig_pos not in self.b.keys():
        return False
      if dest_pos in self.b.keys():
        return False
      piece = self.b[orig_pos]

    # White
    if player == 'w':
      if orig_pos not in self.w.keys():
        return False
      if dest_pos in self.w.keys():
        return False
      piece = self.w[orig_pos]

    # Knight
    if piece == 'n':
      # Unallowed moves
      if not((abs(orig_pos[0]-dest_pos[0])==2 and abs(orig_pos[1]-dest_pos[1])==1) or \
         (abs(orig_pos[1]-dest_pos[1])==2 and abs(orig_pos[0]-dest_pos[0])==1)):
         return False
    # Check validty of the movement according to its piece
    # Pond
    elif piece == 'p':
      # Black pond
      if player == 'b':
        # It can only move forward
        if (orig_pos[0] + 1 != dest_pos[0]): 
          return False
        opponents = self.w.keys()
      # White pond
      elif player == 'w':
        # It can only move forward
        if (orig_pos[0] - 1 != dest_pos[0]): 
          return False
        opponents = self.b.keys()
      # Can't have anything in front of it when moving forward
      if (orig_pos[1] == dest_pos[1]) and (dest_pos in opponents):
        return False
      # Can't move diagnolly without catching another piece
      elif (orig_pos[1] + 1 == dest_pos[1] or orig_pos[1] - 1 == dest_pos[1]) and \
           (dest_pos not in opponents):
        return False
    # King
    # Currently there's no limit I could think of
    #elif piece == 'k':

    # It's now either luke, bishop, or queen
    # There cannot be anything in between orig_pos and dest_pos
    steps = []
    if orig_pos[0] == dest_pos[0]:
      small = min(orig_pos[1], dest_pos[1])
      large = max(orig_pos[1], dest_pos[1])
      steps = [(orig_pos[0], c) for c in range(small + 1, large)]
    elif orig_pos[1] == dest_pos[1]:
      small = min(orig_pos[0], dest_pos[0])
      large = max(orig_pos[0], dest_pos[0])
      steps = [(r, orig_pos[1]) for r in range(small + 1, large)]
    
    for step in steps:
      if step in self.b.keys() or step in self.w.keys():
        return False

    # Luke
    if piece == 'l':
      # Allows moves that are only vertical or horizontal
      if orig_pos[0] != dest_pos[0] or orig_pos[1] != dest_pos[1]:
        return False
    # Bishop
    elif piece == 'b':
      # It can only move diagonally
      if abs(orig_pos[0] - dest_pos[0]) != abs(orig_pos[1] - dest_pos[1]):
        return False
    # Queen
    elif piece == 'q':
      # Allows moves that are vertical, horizontal, or diagonal only
      if not ((orig_pos[0] == dest_pos[0] or orig_pos[1] == dest_pos[1]) or \
          (abs(orig_pos[0] - dest_pos[0]) != abs(orig_pos[1] - dest_pos[1]))):
        return False

    return True

  def can_move(self, player, piece, orig_pos):
    possible_moves = []

    if piece == 'p':
      if player == 'b':
        possible_moves.append((orig_pos[0]+1, orig_pos[1]))
        possible_moves.append((orig_pos[0]+1, orig_pos[1]+1))
        possible_moves.append((orig_pos[0]+1, orig_pos[1]-1))
      elif player == 'w':
        possible_moves.append((orig_pos[0]-1, orig_pos[1]))
        possible_moves.append((orig_pos[0]-1, orig_pos[1]+1))
        possible_moves.append((orig_pos[0]-1, orig_pos[1]-1))

    if piece == 'l' or piece == 'k':
      # Row check
      for i in range(8):
        possible_moves.append(orig_pos[0], i)
      # Column check
      for i in range(8):
        possible_moves.append(i, orig_pos[1])

    if piece == 'n':
      possible_moves = [(orig_pos[0]+2,orig_pos[1]+1),(orig_pos[0]+2,orig_pos[1]-1),\
                        (orig_pos[0]-2,orig_pos[1]+1),(orig_pos[0]-2,orig_pos[1]+1),\
                        (orig_pos[0]+1,orig_pos[1]+2),(orig_pos[0]-1,orig_pos[1]+2),\
                        (orig_pos[0]+1,orig_pos[1]-2),(orig_pos[0]-1,orig_pos[1]-2),]

    if piece == 'b' or piece == 'k':
      # top-right direction
      new_pos = (orig_pos[0]-1, orig_pos[1]+1)
      while new_pos[0] >= 0 and new_pos[1] < 8:
        possible_moves.append(new_pos)
        new_pos = (new_pos[0]-1, new_pos[1]+1)
      # top-left direction
      new_pos = (orig_pos[0]-1, orig_pos[1]-1)
      while new_pos[0] >= 0 and new_pos[1] >= 0:
        possible_moves.append(new_pos)
        new_pos = (new_pos[0]-1, new_pos[1]-1)
      # bottom-right direction
      new_pos = (orig_pos[0]+1, orig_pos[1]+1)
      while new_pos[0] < 8 and new_pos[1] < 8:
        possible_moves.append(new_pos)
        new_pos = (new_pos[0]+1, new_pos[1]+1)
      # bottom-left direction
      new_pos = (orig_pos[0]+1, orig_pos[1]+1)
      while new_pos[0] < 8 and new_pos[1] < 8:
        possible_moves.append(new_pos)
        new_pos = (new_pos[0]+1, new_pos[1]+1)

    if piece == 'k':
      possible_moves = [(orig_pos[0]+1,orig_pos[1]),(orig_pos[0]-1,orig_pos[1]),\
                        (orig_pos[0],orig_pos[1]+1),(orig_pos[0],orig_pos[1]-1)]

    i = 0

    print('orig: ', orig_pos)
    print('possible: ', possible_moves)
    while i < len(possible_moves):
      if self.is_valid_move(player, orig_pos, possible_moves[i]):
        i += 1
      else:
        possible_moves.pop(i)

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
