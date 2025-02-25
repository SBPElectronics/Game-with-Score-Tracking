import json
import random

# Function to load questions from the JSON file
def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ Error: 'questions.json' is either missing or incorrectly formatted!")
        return []

# Function to ask questions and get user's input
def ask_questions(questions):
    score = 0
    random.shuffle(questions)  # Shuffle the question order

    for question in questions:
        print("\n" + question["question"])
        for i, option in enumerate(question["options"], 1):
            print(f"{i}. {option}")

        try:
            user_answer = int(input("Enter your choice (1-4): "))
            chosen_option = question["options"][user_answer - 1].strip()  # Get full answer text
            correct_answer = question["answer"].strip()  # Get correct answer

            if chosen_option == correct_answer:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Wrong! The correct answer was: {question['answer']}")
        except (ValueError, IndexError):
            print("⚠️ Invalid input! Please enter a number between 1 and 4.")

    return score

# Function to initialize scores.json if it's missing or corrupted
def initialize_scores():
    try:
        with open("scores.json", "r", encoding="utf-8") as file:
            json.load(file)  # Check if JSON is valid
    except (FileNotFoundError, json.JSONDecodeError):
        # Create an empty structure if file doesn't exist or is corrupted
        with open("scores.json", "w", encoding="utf-8") as file:
            json.dump({"score_list": []}, file, indent=4)

# Function to save a player's score to the JSON file
def save_score(player_name, score):
    try:
        with open("scores.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"score_list": []}

    # Add the new score
    data["score_list"].append({"player_name": player_name, "score": score})

    # Save back to file
    with open("scores.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Function to display top 5 high scores
def display_high_scores():
    try:
        with open("scores.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("\n⚠️ No scores available!")
        return

    scores = sorted(data["score_list"], key=lambda x: x["score"], reverse=True)[:5]

    print("\n🏆 High Scores 🏆")
    for rank, entry in enumerate(scores, start=1):
        print(f"{rank}. {entry['player_name']}: {entry['score']} points")

# Function to print the full score database
def print_full_database():
    try:
        with open("scores.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("\n⚠️ No scores available!")
        return

    print("\n📜 FULL SCORE DATABASE 📜")
    for entry in sorted(data["score_list"], key=lambda x: x["score"], reverse=True):
        print(f"Player: {entry['player_name']}, Score: {entry['score']}")

# Main function to start the game
def main():
    print("🎯 Welcome to the Quiz Game!")
    questions = load_questions()
    
    if not questions:
        print("⚠️ No questions available! Please check 'questions.json'.")
        return

    score = ask_questions(questions)
    print(f"\n🏆 Your score is {score} out of {len(questions)}!")

    player_name = input("\nEnter your name: ").strip()  # Ask for player's name after the quiz is done
    save_score(player_name, score)
    display_high_scores()

if __name__ == "__main__":
    initialize_scores()  # Ensure the scores file exists and is initialized
    main()
