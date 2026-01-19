import csv, os
from statistics import mean, stdev
from scipy.stats import ttest_ind

def get_pvalue(sample_a: list, sample_b: list) -> float:
    mean_a = mean(sample_a)
    mean_b = mean(sample_b)

    alt = "less" if mean_a < mean_b else "greater"

    result = ttest_ind(sample_a, sample_b, alternative=alt)
    return result.pvalue

results = []

for file in os.scandir("data/"): # scans 'data/' directory
    if not file.is_file():
        continue

    if not file.name.endswith("-results.csv"): # filter for results csv's
        continue

    base = file.name.replace("-results.csv", "")
    threshold_str, opponent = base.split("-")
    threshold = float(threshold_str)

    with open(file, "r") as results_file:
        results_reader = csv.DictReader(results_file)

        adaptivebot_points = []
        opponent_points = []
        adaptivebot_wins = 0
        opponent_wins = 0
        adaptivebot_score = []

        for row in results_reader:
            opponent = row["opponent"]
            winner = row["winner"]
            game_points = int(row["game_points"])
            score = int(row["score"])

            if winner == "AdaptiveBot":
                adaptivebot_points.append(game_points)
                opponent_points.append(0)
                adaptivebot_wins += 1
                adaptivebot_score.append(score)
            else:
                adaptivebot_points.append(0)
                opponent_points.append(game_points)
                opponent_wins += 1
        
        pvalue = get_pvalue(adaptivebot_points, opponent_points)
        winrate = (adaptivebot_wins / opponent_wins)
        mean_score = mean(adaptivebot_score)
        std_dev = stdev(adaptivebot_score)

        # append results as dictionary inside of list
        results.append({
            "threshold": threshold,
            "opponent": opponent,
            "pvalue": round(pvalue, 5),
            "winrate": round(winrate, 3),
            "mean_score": round(mean_score, 3),
            "std_dev": round(std_dev, 3)
            })

# write to file
with open("data/summary.csv", "w", newline="") as summary_file:
    writer = csv.DictWriter(summary_file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)