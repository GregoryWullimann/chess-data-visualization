# Author: Gregory Wullimann,
# Date:   12/12/2021
# Description: This program takes in a list of games and outputs a histogram of players ELO ratings
# Usage: python3 elo_rating_distribution.py --pgn <filename>
# Example: python3 elo_rating_distribution.py --pgn chess.pgn
#          python3 elo_rating_distribution.py --help
# Dataset: https://database.lichess.org/

import matplotlib.pyplot as plt
import seaborn as sns
from utils import get_parse_args

from GameIterator import GameIterator

args = get_parse_args()

games = GameIterator(
    args.pgn,
    args.min_elo_rating,
    args.max_elo_rating,
    args.termination_type,
    args.winner,
    args.number_of_games,
)

def generate_elo_distribution(data):
    sns.set(style="whitegrid")
    sns.histplot(data, kde=False, bins=100)
    plt.xlabel("Elo Rating")
    plt.ylabel("Number of players")
    plt.title("Elo Rating Distribution")
    plt.show()


opening_stats = {}
elos = []
for game in games:
    whiteElo = game.whiteElo
    blackElo = game.blackElo
    if whiteElo > 0:
        elos.append(whiteElo)
    if blackElo > 0:
        elos.append(blackElo)


generate_elo_distribution(elos)
