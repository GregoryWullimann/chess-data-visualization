# Author: Gregory Wullimann,
# Date:   12/12/2021
# Description: This program takes in a list of games and outputs a heatmap of the win rate of ELO ratings against other ELO ratings
# Usage: python3 elo_win_rate.py --pgn <filename>
# Example: python3 elo_win_rate.py --pgn chess.pgn
#          python3 elo_win_rate.py --help
# Dataset: https://database.lichess.org/

import matplotlib.pyplot as plt
import seaborn as sns
from utils import get_parse_args
from GameIterator import GameIterator
import copy

args = get_parse_args()

games = GameIterator(
    args.pgn,
    args.min_elo_rating,
    args.max_elo_rating,
    args.termination_type,
    args.winner,
    args.number_of_games,
)

# Create a matrix where each row is white's Elo rating and each column is black's Elo rating
# ELO are grouped in buckets of bucket_size
def generate_data(bucket_size):
    games_matrix = {}

    for game in games:
        white_elo_rounded = round(game.whiteElo / bucket_size) * bucket_size
        black_elo_rounded = round(game.blackElo / bucket_size) * bucket_size
        if white_elo_rounded not in games_matrix:
            games_matrix[white_elo_rounded] = {}
        if black_elo_rounded not in games_matrix[white_elo_rounded]:
            games_matrix[white_elo_rounded][black_elo_rounded] = {
                "black_wins": 0,
                "white_wins": 0,
                "draws": 0,
            }

        games_matrix[white_elo_rounded][black_elo_rounded][
            "black_wins"
        ] += game.isBlackWinner
        games_matrix[white_elo_rounded][black_elo_rounded][
            "white_wins"
        ] += game.isWhiteWinner
        games_matrix[white_elo_rounded][black_elo_rounded]["draws"] += game.isDraw

    x_labels = sorted([elo for elo in games_matrix.keys()])
    y_labels = []
    for white_elo in games_matrix.values():
        for black_elo in white_elo.keys():
            if black_elo not in y_labels:
                y_labels.append(black_elo)
    y_labels = sorted(y_labels)

    for white_elo in games_matrix:
        for label in y_labels:
            if label not in games_matrix[white_elo]:
                games_matrix[white_elo][label] = {
                    "black_wins": 0,
                    "white_wins": 0,
                    "draws": 0,
                }

    data = []
    for white_elo in sorted(games_matrix):
        data.append([])
        for black_elo in sorted(games_matrix[white_elo]):
            b = games_matrix[white_elo][black_elo]
            total_games = b["black_wins"] + b["white_wins"] + b["draws"]
            if total_games == 0:
                win_rate = -1
            else:
                win_rate = (b["white_wins"] + b["draws"] * 0.5) / total_games
            data[-1].append(win_rate)

    data.reverse()
    y_labels.reverse()
    return data, x_labels, y_labels


def generate_heatmap(data, x_labels, y_labels):
    my_cmap = copy.copy(sns.cm.rocket)
    my_cmap.set_under("#505050")
    sns.set(style="whitegrid")
    sns.heatmap(
        data,
        annot=False,
        cmap=my_cmap,
        xticklabels=x_labels,
        yticklabels=y_labels,
        vmin=0,
    )
    plt.xlabel("Black Elo Rating")
    plt.ylabel("White Elo Rating")
    plt.title("Win rate based on players' Elo ratings")
    plt.show()


bucket_size = 50
data, x_labels, y_labels = generate_data(bucket_size)
generate_heatmap(data, x_labels, y_labels)
