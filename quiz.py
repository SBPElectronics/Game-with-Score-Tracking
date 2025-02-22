import json
import random

#checking if working

# Load questions from JSON file
def load_questions():
    with open("questions.json", "r") as file:
        return json.load(file)

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
            if question["options"][user_answer - 1] == question["answer"]:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Wrong! The correct answer was: {question['answer']}")
        except (ValueError, IndexError):
            print("⚠️ Invalid input! Please enter a number between 1 and 4.")

    return score

# Main function
def main():
    print("🎯 Welcome to the Quiz Game!")
    questions = load_questions()
    score = ask_questions(questions)
    print(f"\n🏆 You scored {score} out of {len(questions)}!")

if __name__ == "__main__":
    main()