# Python Chess Data Analysis

## Dataset

The dataset used is from Lichess (https://database.lichess.org/).
In order to download the same dataset use the following commands, which download and unpack the file in the `./data` folder.

    wget https://database.lichess.org/standard/lichess_db_standard_rated_2017-01.pgn.bz2 -P ./data
    bunzip2 ./data/lichess_db_standard_rated_2017-01.pgn.bz2 

## Requirements
Run the following command to install the dependacies.

    pip3 install -r requirements.txt

## Scripts
There are 4 main script to run, each one will generate a different chart. To each script optional arguments can be passed to filter the dataset.

    python3 elo_rating_distribution.py --help

    usage: elo_rating_distribution.py [-h] --pgn PGN [--min-elo-rating MIN_ELO_RATING] [--max-elo-rating MAX_ELO_RATING] [--termination-type {all,draw,time_forfeit,checkmate,resign}]
                                    [--winner {all,draw,white,black}] [--number-of-games NUMBER_OF_GAMES]

    optional arguments:
    -h, --help            show this help message and exit
    --pgn PGN             PGN file to analyze
    --min-elo-rating MIN_ELO_RATING
                            Filter by minimum elo rating (default: 0)
    --max-elo-rating MAX_ELO_RATING
                            Filter by maxium elo rating (default: None)
    --termination-type {all,draw,time_forfeit,checkmate,resign}
                            Filter by the type of termination (default: all)
    --winner {all,draw,white,black}
                            Minimum rating of the players (default: all)
    --number-of-games NUMBER_OF_GAMES
                            Maximum number of games to analyze)

In order to run a script only a PGN file is required, the other arguments are optional.

    python3 elo_rating_distribution.py --pgn ./data/lichess_db_standard_rated_2017-01.pgn
