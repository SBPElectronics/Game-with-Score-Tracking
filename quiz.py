import json
import random
import sqlite3

# Database connection
conn = sqlite3.connect("quiz_scores.db")
cursor = conn.cursor()

# Create scores table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT,
        score INTEGER
    )
""")
conn.commit()

# Load questions from JSON file
def load_questions():
    try:
        with open("questions.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ Error: questions.json is missing or incorrectly formatted!")
        return []

# Ask questions and get user input
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
            correct_answer = question["answer"].strip()  # Compare full answer

            if chosen_option == correct_answer:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Wrong! The correct answer was: {question['answer']}")
        except (ValueError, IndexError):
            print("⚠️ Invalid input! Please enter a number between 1 and 4.")

    return score

# Save score to database
def save_score(player_name, score):
    cursor.execute("INSERT INTO scores (player_name, score) VALUES (?, ?)", (player_name, score))
    conn.commit()

# Display high scores
def display_high_scores():
    cursor.execute("SELECT player_name, score FROM scores ORDER BY score DESC LIMIT 5")
    scores = cursor.fetchall()

    print("\n🏆 High Scores 🏆")
    for rank, (player, score) in enumerate(scores, start=1):
        print(f"{rank}. {player}: {score} points")

# Print the entire database
def print_full_database():
    cursor.execute("SELECT * FROM scores ORDER BY score DESC")
    scores = cursor.fetchall()

    print("\n📜 FULL SCORE DATABASE 📜")
    for row in scores:
        print(f"ID: {row[0]}, Player: {row[1]}, Score: {row[2]}")

# Main function
def main():
    print("🎯 Welcome to the Quiz Game!")
    player_name = input("Enter your name: ")

    questions = load_questions()
    if not questions:
        print("⚠️ No questions found! Please check questions.json.")
        return

    score = ask_questions(questions)
    print(f"\n🏆 {player_name}, you scored {score} out of {len(questions)}!")

    # Save and display scores
    save_score(player_name, score)
    display_high_scores()

    # Print full database after game
    print_full_database()

if __name__ == "__main__":
    main()

    # Close database connection
    conn.close()
