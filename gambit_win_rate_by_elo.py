# Author: Gregory Wullimann,
# Date:   12/12/2021
# Description: This program takes in a list of games and outputs a line plot of the win rate of Gambits for each ELO rating
# Usage: python3 gambit_win_rate_by_elo.py --pgn <filename>
# Example: python3 gambit_win_rate_by_elo.py --pgn chess.pgn
#          python3 gambit_win_rate_by_elo.py --help
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

opening_stats = {}
buckets = {}
for game in games:
    elo_game_rounded = round(game.elo / 50) * 50
    opening = game.headers["Opening"]
    if not "gambit" in opening.lower():
        continue
    gambit_name = opening.split("Gambit")[0].strip() + " Gambit"

    if gambit_name not in buckets:
        buckets[gambit_name] = {"elos": {}, "count": 0}
    for gambit in buckets:
        if elo_game_rounded not in buckets[gambit]["elos"]:
            buckets[gambit]["elos"][elo_game_rounded] = {
                "black_win": 0,
                "white_win": 0,
                "draw": 0,
                "count": 0,
            }

    buckets[gambit_name]["elos"][elo_game_rounded]["white_win"] += game.isWhiteWinner
    buckets[gambit_name]["elos"][elo_game_rounded]["black_win"] += game.isBlackWinner
    buckets[gambit_name]["elos"][elo_game_rounded]["draw"] += game.isDraw
    buckets[gambit_name]["elos"][elo_game_rounded]["count"] += 1
    buckets[gambit_name]["count"] += 1

sorted_buckets = sorted(buckets.items(), key=lambda x: x[1]["count"], reverse=True)
sorted_buckets = sorted_buckets[:10]

sorted_buckets = dict(sorted_buckets)


lines = []
x = []
y = []

for opening in sorted_buckets:
    opening_ = sorted_buckets[opening]
    lines.append(opening)
    elos = []
    win_rates = []
    for elo in sorted(opening_["elos"].keys()):
        elos.append(elo)
        if opening_["elos"][elo]["count"] > 5:
            win_rate = (
                opening_["elos"][elo]["white_win"] + opening_["elos"][elo]["draw"] * 0.5
            ) / opening_["elos"][elo]["count"]
        else:
            win_rate = None
        win_rates.append(win_rate)
    x.append(elos)
    y.append(win_rates)


def generate_line_plot(lines, x, y):

    sns.set(style="whitegrid")
    for i, line in enumerate(lines):
        plt.plot(x[i], y[i], label=line)
    plt.axhline(y=0.5, color='black', linestyle='dashed')
    plt.ylim([0, 1])
    plt.xlabel("Elo Rating")
    plt.ylabel("Win rate")
    plt.title("Win rate of Gambits by Elo Rating")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

generate_line_plot(lines, x, y)