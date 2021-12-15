from Game import Game
import os.path

# GameIterator Class to iterate over all games in a PGN file
# an iterator is used instead of a list because the PGN file is large
class GameIterator:
    def __init__(
        self,
        pgn_path,
        minElo,
        maxElo,
        winnerFilter,
        termination_type,
        numbers_of_games=None,
    ):
        self.pgn_path = pgn_path
        self.minElo = minElo
        self.maxElo = maxElo
        self.winnerFilter = winnerFilter
        self.termination_type = termination_type
        self.numbers_of_games = numbers_of_games
        self.games = []
        self.headers = {}
        self.moves = None
        self.pgn = None
        if os.path.isfile(self.pgn_path):
            self.pgn = open(self.pgn_path, "r")
        else:
            print(f"File {self.pgn_path} does not exist")
            exit()

        self.processed = 0

    def __iter__(self):
        headers = {}
        moves = None
        line = self.pgn.readline()
        # Parse each line in order to create a game object
        while line:
            if (
                self.numbers_of_games is not None
                and self.processed > self.numbers_of_games
            ):
                return None
            if line.startswith("["):
                header = self.__parse_header(line)
                headers[header[0]] = header[1]
            elif line.startswith("1."):
                moves = line.strip("\n").strip("\r")
                if any(x in moves for x in ["%clk", "%eval"]):
                    moves = None
                    headers = {}
                    line = self.pgn.readline()
                    continue
            elif line.strip("\n").strip("\r") == "" and moves != None:
                game = Game(moves, headers)
                if self.__is_valid_game(game):
                    self.processed += 1
                    yield game
                moves = None
                headers = {}
            line = self.pgn.readline()

    def __parse_header(self, line):
        header = line.strip("\n").strip("\r").strip("[").strip("]").split(" ")
        header[0] = header[0].strip('"')
        header[1] = " ".join(header[1:]).strip('"')
        return header

    # Check if the game is valid given the filters
    def __is_valid_game(self, game):
        headers = game.headers
        if headers is None or headers == {}:
            return False

        if self.minElo > game.minElo:
            return False

        if self.maxElo is not None and self.maxElo < game.maxElo:
            return False

        isTerminationType = (
            self.termination_type == "all"
            or self.termination_type == "checkmate"
            and game.isCheckmate
            or self.termination_type == "resign"
            and game.isResign
            or self.termination_type == "time_forfeit"
            and game.isTimeForfeit
        )
        if not isTerminationType:
            return False

        isValidWinner = (
            self.winnerFilter == "all"
            or (game.isWhiteWinner and self.winnerFilter == "white")
            or (game.isBlackWinner and self.winnerFilter == "black")
            or (game.isDraw and self.winnerFilter == "draw")
        )
        if not isValidWinner:
            return False

        return True
