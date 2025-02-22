import json

SCORE_FILE = "score.json"  # Stores player scores

# Load existing scores
def load_scores():
    try:
        with open(SCORE_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save a new score
def save_score(player_name, score):
    scores = load_scores()
    scores[player_name] = score  # Update or add player's score

    with open(SCORE_FILE, "w") as file:
        json.dump(scores, file, indent=4)

# Display high scores
def display_high_scores():
    scores = load_scores()
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    print("\n🏆 High Scores 🏆")
    for rank, (player, score) in enumerate(sorted_scores, start=1):
        print(f"{rank}. {player}: {score} points")
