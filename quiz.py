import json
import random

# Function to load questions from the JSON file
def load_questions():
    try:
        with open("questions.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ Error: 'questions.json' is either missing or incorrectly formatted!")
        return []

# Function to ask questions and get user's input
def ask_questions(questions):
    score = 0
    random.shuffle(questions)  # Shuffle the question order

    # Select the first 5 random questions
    selected_questions = questions[:5]

    for question in selected_questions:
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

# Function to save player's score to scores.json
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

# Function to display high scores from scores.json
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

# Main function to start the game
def main():
    print("🎯 Welcome to the Islamic Quiz Game!")
    
    # Display menu with options
    print("\nPlease choose an option:")
    print("1. Take the Quiz")
    print("2. View the Leaderboard")
    
    try:
        choice = int(input("\nEnter 1 or 2: "))
        
        if choice == 1:
            # Load questions
            questions = load_questions()
            
            if not questions:
                print("⚠️ No questions available! Please check 'questions.json'.")
                return
            
            # Ask questions and calculate the score
            score = ask_questions(questions)
            print(f"\n🏆 Your score is {score} out of 5!")
            
            # Ask for player's name and save score
            player_name = input("\nEnter your name: ").strip()
            save_score(player_name, score)
            print("\nYour score has been saved!")
        
        elif choice == 2:
            # Display high scores
            display_high_scores()
        
        else:
            print("⚠️ Invalid choice! Please enter 1 or 2.")
            
    except ValueError:
        print("⚠️ Invalid input! Please enter a number (1 or 2).")

# Run the program
if __name__ == "__main__":
    main()
