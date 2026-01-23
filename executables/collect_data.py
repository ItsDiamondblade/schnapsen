from schnapsen.bots import AdaptiveBot, RandBot, BullyBot, RdeepBot
from schnapsen.game import SchnapsenGamePlayEngine, Bot
import random, csv

thresholds: list[float] = [0, 0.25, 0.5, 0.75, 1]
opponents: list[Bot] = [RandBot, BullyBot, RdeepBot]
trials = 500

engine = SchnapsenGamePlayEngine()

def make_seed(opponent_name: str, trial: int): # makes seed so that it's the same per bot per trial
    return hash((opponent_name, trial)) & 0xFFFFFFFF

#running tests, writing to files
for threshold in thresholds:
    adaptive_bot = AdaptiveBot(threshold, "AdaptiveBot")
        # Loop through opponent bots
    for opponent in opponents:
        opponent_name = opponent.__name__
        with open(f"./data/{threshold}-{opponent_name}-results.csv", "w+", newline="") as results_file:
            writer = csv.writer(results_file)
            writer.writerow(["trial","opponent", "seed", "opponent_rng", "winner", "game_points", "score", "aggressive_moves", "defensive_moves"])
            # Use a loop to run 10 games
            for trial in range(1, trials + 1):
                aggressive_moves = 0
                defensive_moves = 0
                seed = make_seed(opponent_name, trial)
                game_rng = random.Random(seed)
                opponent_rng = random.Random(seed + 1) # seed + 1 so they're not synchronized

                if opponent is RdeepBot:
                    opponent_bot = RdeepBot(num_samples=12, depth=5, rand=opponent_rng, name=opponent_name)
                else:
                    opponent_bot = opponent(opponent_rng, opponent_name)

                # Run a game at each iteration of the loop and store the data
                winner, game_points, score = engine.play_game(adaptive_bot, opponent_bot, game_rng)
                aggressive_moves += adaptive_bot.aggressive_moves
                defensive_moves += adaptive_bot.defensive_moves
                writer.writerow([trial, opponent_name, seed, seed + 1, str(winner), game_points, score.direct_points, aggressive_moves, defensive_moves])
        print(f"Successfully wrote: {threshold}-{opponent_name}")