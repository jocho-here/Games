class Board():
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
      
  def move(self, player, orig_pos, dest_pos):
    if self.is_valid_move(player, orig_pos, dest_pos):
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

      # DEBUG
      print(self)

      return True
    
    return False

#  def start_game(self):
#    while True:
#      1000k

#  def test_move_validity(self):
