# Game Class to store game's moves and headers
class Game:
    def __init__(self, moves, headers):
        self.moves = moves
        self.white_moves = self.moves.split()[1::3]
        self.number_of_moves = len(self.white_moves)
        self.white_moves = [Move(move) for move in self.white_moves[:-1]]
        self.black_moves = self.moves.split()[2::3]
        self.black_moves = [Move(move) for move in self.black_moves[:-1]]
        self.headers = headers
    
    @property
    def isWhiteWinner(self):
        return self.headers['Result'] == '1-0'
    
    @property
    def isBlackWinner(self):
        return self.headers['Result'] == '0-1'
    
    @property
    def isDraw(self):
        return self.headers['Result'] == '1/2-1/2'
    
    @property
    def isCheckmate(self):
        return self.moves.endswith('# 1-0') or self.moves.endswith('# 0-1')

    @property
    def whiteElo(self):
        whiteElo = self.headers.get('WhiteElo', '?')
        return int(whiteElo) if whiteElo != '?' else 0

    @property
    def blackElo(self):
        blackElo = self.headers.get('BlackElo', '?')
        return int(blackElo) if blackElo != '?' else 0

    @property
    def minElo(self):
        return min(self.whiteElo, self.blackElo)

    @property
    def maxElo(self):
        return max(self.whiteElo, self.blackElo)
    
    @property
    def elo(self):
        return (self.whiteElo + self.blackElo) / 2

    @property
    def isResign(self):
        return not self.isCheckmate and self.headers.get('Termination', '') == 'Normal'
    
    @property
    def isTimeForfeit(self):
        return self.headers.get('Termination', '') == 'Time forfeit'
    
    def __str__(self):
        return self.moves

# Move class which stores move's information, such as target coordinates, piece type, etc.
class Move:
    def __init__(self, move):
        self.move = move
        self.isPawn = self.move.startswith(('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'))
        self.isCastle = self.move[0] == 'O'
        self.isPromotion = "=" in self.move
        self.isCheck = "+" in self.move
        self.isCapture = "x" in self.move
        self.isCheckmate = "#" in self.move
        self.piece = "P" if self.isPawn else self.move[0]

        if self.isCastle:
            self.row = None
            self.col = None
        elif (self.isCheck or self.isCheckmate) and not self.isPromotion:
            self.row = self.move[-2]
            self.col = self.move[-3]
        elif (self.isCheck or self.isCheckmate) and self.isPromotion:
            self.row = self.move[-4]
            self.col = self.move[-5]
        elif self.isPromotion:
            self.row = self.move[-3]
            self.col = self.move[-4]
        else:
            self.row = self.move[-1]
            self.col = self.move[-2]

    @property
    def colIndex(self):
        return ord(self.col) - ord('a')
    
    @property
    def rowIndex(self):
        return int(self.row) - 1