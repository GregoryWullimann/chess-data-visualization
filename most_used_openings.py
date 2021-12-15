# Author: Gregory Wullimann,
# Date:   12/12/2021
# Description:
# Usage: python3 elo_rating_distribution.py --pgn <filename>
# Example: python3 elo_rating_distribution.py --pgn chess.pgn
#          python3 elo_rating_distribution.py --help
# Dataset: https://database.lichess.org/

import matplotlib.pyplot as plt
import seaborn as sns
from utils import get_parse_args, import_games

args = get_parse_args()

games = import_games(
    args.pgn,
    args.min_elo_rating,
    args.max_elo_rating,
    args.termination_type,
    args.winner,
    args.number_of_games,
)
print(f"Found {len(games)} games")

def generate_bar_chart(data):
    # create histogram
    data_sorted = sorted(data.items(), key=lambda x: x[1], reverse=True)
    data_sorted = data_sorted[:10]
    x = [val[0] for val in data_sorted]
    y = [val[1] for val in data_sorted]
    sns.set(style="whitegrid")
    sns.barplot(x=y, y=x, orient = 'h')
    plt.ylabel("Opening name")
    plt.xlabel("Count")
    plt.title("Most used opening")
    plt.show()

opening_stats = {}
for game in games:
    opening = game.headers.get('Opening')
    if opening not in opening_stats:
        opening_stats[opening] = 1
    else:
        opening_stats[opening] += 1


generate_bar_chart(opening_stats)

