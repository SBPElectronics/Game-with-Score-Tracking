import json
import random
import tkinter as tk
from tkinter import messagebox

# Load questions from the JSON file
def load_questions():
    try:
        with open("questions.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "❌ 'questions.json' is missing or incorrectly formatted!")
        return []

# Save player's score to scores.json
def save_score(player_name, score):
    try:
        with open("scores.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"score_list": []}

    data["score_list"].append({"player_name": player_name, "score": score})

    with open("scores.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Show leaderboard (high scores)
def display_high_scores():
    try:
        with open("scores.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showinfo("Leaderboard", "⚠️ No scores available!")
        return

    scores = sorted(data["score_list"], key=lambda x: x["score"], reverse=True)[:5]
    leaderboard_text = "\n🏆 High Scores 🏆\n" + "\n".join(f"{i+1}. {entry['player_name']}: {entry['score']} points" for i, entry in enumerate(scores))
    
    messagebox.showinfo("Leaderboard", leaderboard_text)

# Start the quiz
def start_quiz():
    global score, current_question_index, questions, selected_questions

    questions = load_questions()
    if not questions:
        return

    random.shuffle(questions)
    selected_questions = questions[:5]
    score = 0
    current_question_index = 0
    show_question()

# Show a question
def show_question():
    global current_question_index

    if current_question_index < len(selected_questions):
        question = selected_questions[current_question_index]
        question_label.config(text=question["question"])

        for i in range(4):
            option_buttons[i].config(text=question["options"][i], state="normal")

    else:
        end_quiz()

# Handle answer selection
def check_answer(choice):
    global score, current_question_index

    question = selected_questions[current_question_index]
    chosen_option = question["options"][choice]
    
    if chosen_option == question["answer"]:
        score += 1

    current_question_index += 1
    show_question()

# End the quiz and ask for player’s name
def end_quiz():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Please enter your name before starting the quiz.")
        return
    
    messagebox.showinfo("Quiz Completed", f"🏆 Your score is {score} out of 5!")
    save_score(name, score)

# Create GUI window
root = tk.Tk()
root.title("Islamic Quiz Game")
root.geometry("500x500")
root.config(bg="#f4f4f4")

# Title
title_label = tk.Label(root, text="🎯 Islamic Quiz Game", font=("Arial", 16, "bold"), bg="#f4f4f4", fg="green")
title_label.pack(pady=10)

# Name Entry
name_label = tk.Label(root, text="Enter Your Name:", font=("Arial", 12), bg="#f4f4f4")
name_label.pack()
name_entry = tk.Entry(root, font=("Arial", 12))
name_entry.pack(pady=5)

# Start Quiz Button
start_button = tk.Button(root, text="Start Quiz", font=("Arial", 12, "bold"), bg="blue", fg="white", command=start_quiz)
start_button.pack(pady=10)

# Question Label
question_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#f4f4f4", wraplength=400, justify="center")
question_label.pack(pady=20)

# Option Buttons
option_buttons = []
for i in range(4):
    btn = tk.Button(root, text="", font=("Arial", 12), width=40, bg="white", command=lambda i=i: check_answer(i))
    btn.pack(pady=5)
    option_buttons.append(btn)

# View Leaderboard Button
leaderboard_button = tk.Button(root, text="🏆 View Leaderboard", font=("Arial", 12, "bold"), bg="orange", command=display_high_scores)
leaderboard_button.pack(pady=10)

# Run the GUI
root.mainloop()
