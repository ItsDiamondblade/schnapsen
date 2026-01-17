from schnapsen.bots import AdaptiveBot, RandBot, BullyBot, RdeepBot
from schnapsen.game import SchnapsenGamePlayEngine, Bot
import random, csv

thresholds: list[float] = [0, 0.5, 1]
opponents: list[Bot] = [RandBot, BullyBot, RdeepBot]
trials = 10

engine = SchnapsenGamePlayEngine()

def make_seed(opponent_name: str, trial: int): # makes seed so that it's the same per bot per trial
    return hash((opponent_name, trial)) & 0xFFFFFFFF

#running tests, writing to files
for threshold in thresholds:
    adaptive_bot = AdaptiveBot(threshold, "AdaptiveBot")
    with open(f"./data/{threshold}-results.csv", "w+", newline="") as results_file:
        writer = csv.writer(results_file)
        writer.writerow(["trial","opponent", "seed", "opponent_rng", "winner", "game_points", "score"])
        # Loop through opponent bots
        for opponent in opponents:
            opponent_name = opponent.__name__
            # Use a loop to run 10 games
            for trial in range(1, trials + 1):
                seed = make_seed(opponent_name, trial)
                game_rng = random.Random(seed)
                opponent_rng = random.Random(seed + 1) # seed + 1 so they're not synchronized

                if opponent is RdeepBot:
                    opponent_bot = RdeepBot(num_samples=12, depth=5, rand=opponent_rng, name=opponent_name)
                else:
                    opponent_bot = opponent(opponent_rng, opponent_name)

                # Run a game at each iteration of the loop and store the data
                winner, game_points, score = engine.play_game(adaptive_bot, opponent_bot, game_rng)
                writer.writerow([trial, opponent_name, seed, seed + 1, str(winner), game_points, score.direct_points])
    print(f"Successfully wrote treshold: {threshold}")

# getting averages
# with open(f"./data/summary.csv", "w+") as summary_file:
#     summary_writer = csv.writer(summary_file)
#     summary_writer.writerow(opponents)
#     for threshold in [0.5]:
#         totals = {}
#         for opponent in opponents:
#             totals[opponent] = {total_game_points: 0, total_score: 0}
#         with open(f"./data/{threshold}-results.csv", "w+") as results_file:
#             reader = csv.DictReader(results_file)
#             for row in reader:
#                 opponent = row["opponent"]
#                 winner = row["winner"]
#                 game_points = row["game_points"]
#                 score = row["score"]

#                 totals[opponent][total_game_points] += game_points
#                 totals[opponent][total_score] += score