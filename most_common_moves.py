# Author: Gregory Wullimann,
# Date:   12/12/2021
# Description: This program generates a heatmap of the most common moves by piece.
# Usage: python3 most_common_moves.py --pgn <filename>
# Example: python3 most_common_moves.py --pgn chess.pgn
#          python3 most_common_moves.py --help
# Dataset: https://database.lichess.org/

import matplotlib.pyplot as plt
import seaborn as sns
from GameIterator import GameIterator

from utils import generate_square_matrix, get_parse_args

args = get_parse_args()

games = GameIterator(
    args.pgn,
    args.min_elo_rating,
    args.max_elo_rating,
    args.termination_type,
    args.winner,
    args.number_of_games,
)


def generate_heatmap(data):
    X_LABELS = ["A", "B", "C", "D", "E", "F", "G", "H"]
    Y_LABELS = [1, 2, 3, 4, 5, 6, 7, 8]
     
    fig,(r1, r2) = plt.subplots(2,3,sharey="none")
    fig.suptitle('Most frequent moves by piece')
    sns.heatmap(data['Q'], ax=r1[0], xticklabels=X_LABELS, yticklabels=Y_LABELS)
    sns.heatmap(data['K'], ax=r1[1], xticklabels=X_LABELS, yticklabels=Y_LABELS)
    sns.heatmap(data['P'], ax=r1[2], xticklabels=X_LABELS, yticklabels=Y_LABELS)
    sns.heatmap(data['R'], ax=r2[0], xticklabels=X_LABELS, yticklabels=Y_LABELS)
    sns.heatmap(data['N'], ax=r2[1], xticklabels=X_LABELS, yticklabels=Y_LABELS)
    sns.heatmap(data['B'], ax=r2[2], xticklabels=X_LABELS, yticklabels=Y_LABELS)
    r1[0].invert_yaxis()
    r1[0].set_title('Queen')
    r1[1].invert_yaxis()
    r1[1].set_title('King')
    r1[2].invert_yaxis()
    r1[2].set_title('Pawn')
    r2[0].invert_yaxis()
    r2[0].set_title('Rook')
    r2[1].invert_yaxis()
    r2[1].set_title('Knight')
    r2[2].invert_yaxis()
    r2[2].set_title('Bishop')
    plt.show()

heatmaps_position_data = {
    "Q": generate_square_matrix(8),
    "R": generate_square_matrix(8),
    "B": generate_square_matrix(8),
    "N": generate_square_matrix(8),
    "P": generate_square_matrix(8),
    "K": generate_square_matrix(8),
}

for game in games:
    for turn, move in enumerate(game.white_moves):
        if move.piece in heatmaps_position_data:
            heatmaps_position_data[move.piece][move.rowIndex][move.colIndex] += 1

generate_heatmap(heatmaps_position_data)
