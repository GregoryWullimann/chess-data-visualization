import argparse

def generate_square_matrix(n):
    return [[0 for x in range(n)] for y in range(n)]

def get_parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pgn",
        help="PGN file to analyze",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--min-elo-rating",
        help="Filter by minimum elo rating (default: 0)",
        default=0,
        type=int,
    )
    parser.add_argument(
        "--max-elo-rating",
        help="Filter by maxium elo rating (default: None)",
        default=None,
        type=int,
    )
    parser.add_argument(
        "--termination-type",
        help="Filter by the type of termination (default: all)",
        choices=["all", "draw", "time_forfeit", "checkmate", "resign"],
        default="all",
    )
    parser.add_argument(
        "--winner",
        help="Minimum rating of the players (default: all)",
        choices=["all", "draw", "white", "black"],
        default="all",
    )

    parser.add_argument(
        "--number-of-games",
        help="Maximum number of games to analyze)",
        type=int,
        default=None,
    )

    return parser.parse_args()