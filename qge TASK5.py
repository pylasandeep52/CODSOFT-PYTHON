import tkinter as tk
from tkinter import messagebox
import random

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("400x400")

        self.quiz_questions = [
            {
                "question": "What is the largest ocean on Earth?",
                "choices": ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean"],
                "correct_answer": "Pacific Ocean"
            },
            {
                "question": "What is the capital of France?",
                "choices": ["London", "Paris", "Berlin", "Madrid"],
                "correct_answer": "Paris"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "choices": ["Venus", "Mars", "Jupiter", "Neptune"],
                "correct_answer": "Mars"
            },
            {
                "question": "What is the capital city of Japan?",
                "choices": ["Tokyo", "Beijing", "Seoul", "Bangkok"],
                "correct_answer": " Tokyo"
            },
             {
                "question": "Who is the author of the famous play Romeo and Juliet?",
                "choices": ["William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain"],
                "correct_answer": "William Shakespeare"
            },
            {
                "question": "What is the tallest mountain in the world?",
                "choices": ["Mount Kilimanjaro", "Mount Everest", "Mount McKinley (Denali)", "Mount Fuji"],
                "correct_answer": "Mount Everest"
            },
            {
                "question": "Which country is known as the Land of the Rising Sun?",
                "choices": ["Japan", "China", "South Korea", " India"],
                "correct_answer": "Japan"
            }
            # Add more quiz questions here
        ]

        self.current_question = 0
        self.score = 0
        self.user_answers = {}

        self.welcome_label = tk.Label(root, text="Welcome to the Quiz Game.Get ready to test your knowledge!", font=("Helvetica", 20))
        self.welcome_label.pack(pady=20)

        self.rules_label = tk.Label(root, text="Rules:\n1. Read each question carefully.\n2. Select the best answer.\n3. Have fun!", font=("Helvetica", 12))
        self.rules_label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Quiz", command=self.start_quiz, bg='#6dd5ed', fg='#141e30')
        self.start_button.pack(pady=10)

        self.question_label = tk.Label(root, text="", wraplength=300, font=("Helvetica", 16))
        self.choice_var = tk.StringVar()
        self.choice_var.set("")
        self.choices_frame = tk.Frame(root)
        self.feedback_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.next_button = tk.Button(root, text="Next", command=self.next_question, bg='#02aab0', fg='#141e30')

        self.load_question()

        # Marquee Text
        self.marquee_canvas = tk.Canvas(root, bg="white", width=1500, height=30)
        self.marquee_canvas.pack(pady=10)
        self.marquee_text = "QUIZ GAME APPLICATION"
        self.marquee_position = 400
        self.marquee_color = ["red", "green", "blue", "orange", "purple"]
        self.marquee_index = 0
        self.update_marquee()

    def update_marquee(self):
        self.marquee_position -= 2
        if self.marquee_position < -len(self.marquee_text) * 8:
            self.marquee_position = 400
            self.marquee_index = (self.marquee_index + 1) % len(self.marquee_color)
            self.marquee_canvas.itemconfig("marquee", fill=self.marquee_color[self.marquee_index])

        self.marquee_canvas.delete("marquee")
        self.marquee_canvas.create_text(self.marquee_position, 15, text=self.marquee_text, fill=self.marquee_color[self.marquee_index], font=("Helvetica", 14), tags="marquee")
        self.root.after(10, self.update_marquee)

    def start_quiz(self):
        self.welcome_label.pack_forget()
        self.rules_label.pack_forget()
        self.start_button.pack_forget()

        self.question_label.pack(pady=20)
        self.choices_frame.pack(pady=10)
        self.feedback_label.pack(pady=10)
        self.next_button.pack()

    def load_question(self):
        question_data = self.quiz_questions[self.current_question]
        question = question_data["question"]
        choices = question_data["choices"]

        self.question_label.config(text=question)
        self.feedback_label.config(text="")
        self.choice_var.set("")

        for widget in self.choices_frame.winfo_children():
            widget.destroy()

        for choice in choices:
            tk.Radiobutton(self.choices_frame, text=choice, variable=self.choice_var, value=choice).pack(anchor='w')

    def evaluate_answer(self):
        user_choice = self.choice_var.get()
        question_data = self.quiz_questions[self.current_question]
        correct_answer = question_data["correct_answer"]
        self.user_answers[self.current_question] = user_choice

        if user_choice == correct_answer:
            self.score += 1
            return True
        else:
            self.feedback_label.config(text=f"Sorry, that's incorrect. The correct answer is: {correct_answer}")
            return False

    def next_question(self):
        if self.current_question < len(self.quiz_questions) - 1:
            if self.choice_var.get() == "":
                messagebox.showwarning("Warning", "Please select an answer.")
            else:
                if self.evaluate_answer():
                    self.feedback_label.config(text="Correct!")
                else:
                    self.feedback_label.config(text="Incorrect!")
                self.current_question += 1
                self.load_question()
        else:
            if self.choice_var.get() == "":
                messagebox.showwarning("Warning", "Please select an answer.")
            else:
                if self.evaluate_answer():
                    self.feedback_label.config(text="Correct!")
                else:
                    self.feedback_label.config(text="Incorrect!")
                self.display_result()

    def display_result(self):
        self.question_label.config(text="Quiz Completed!")
        self.next_button.pack_forget()

        self.print_performance_message()
        self.feedback_label.config(text=f"Your score: {self.score}/{len(self.quiz_questions)}")

        self.display_correct_answers()
        self.play_again_button = tk.Button(self.root, text="Play Again", command=self.play_again)
        self.play_again_button.pack(pady=10)

    def print_performance_message(self):
        if self.score == len(self.quiz_questions):
            messagebox.showinfo("Quiz Completed", "Congratulations! You answered all questions correctly.")
        elif self.score >= len(self.quiz_questions) // 2:
            messagebox.showinfo("Quiz Completed", "Well done! You did a good job.")
        else:
            messagebox.showinfo("Quiz Completed", "You can do better next time.")

    def display_correct_answers(self):
        result_text = "Correct Answers:\n\n"
        for index, question_data in enumerate(self.quiz_questions):
            question = question_data["question"]
            correct_answer = question_data["correct_answer"]
            user_answer = self.user_answers.get(index, "Not answered")
            result_text += f"Question {index + 1}: {question}\nYour Answer: {user_answer}\nCorrect Answer: {correct_answer}\n\n"
        messagebox.showinfo("Quiz Results", result_text)

    def play_again(self):
        self.current_question = 0
        self.score = 0
        self.user_answers = {}
        self.load_question()
        self.play_again_button.pack_forget()
        self.next_button.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizGame(root)
    root.mainloop()
