import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

def marquee():
    global marquee_offset, color_index
    canvas.coords(text_id, marquee_offset, 10)
    marquee_offset -= 1
    if marquee_offset <= -marquee_text_width:
        marquee_offset = window_width
    canvas.itemconfig(text_id, fill=colors[color_index])  # Change text color
    color_index = (color_index + 1) % len(colors)  # Move to the next color
    canvas.after(3, marquee)  # Update every 3 milliseconds



def generate_password():
    length = int(length_entry.get())
    if length < 8:
        messagebox.showwarning("Warning", "Password length should be at least 8 characters.")
        return

    # Define the characters to be used in the password
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate the password
    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

    # Update the generated password label
    generated_password_label.config(text=f"Generated Password: {password}")

def copy_to_clipboard():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copy to Clipboard", "Password copied to clipboard.")
    else:
        messagebox.showwarning("Warning", "No password to copy.")

def reset_password():
    password_entry.delete(0, tk.END)
    generated_password_label.config(text="Generated Password: ")

def exit_app():
    app.quit()

# Initialize the main window
app = tk.Tk()
app.title("Password Generator")
app.geometry("500x400")

marquee_text = "PASSWORD generator application designed by PYLA SANDEEP"
canvas = tk.Canvas(app, width=1500, height=28)
canvas.pack(pady=15)

# Draw the marquee text on the canvas
text_id = canvas.create_text(1000,3,text=marquee_text, font=('Helvetica', 12), anchor='e', fill='black')

# Measure the width of the marquee text to know when to wrap around
marquee_text_width = canvas.bbox(text_id)[2] - canvas.bbox(text_id)[0]

window_width = 1000
marquee_offset = window_width

# List of colors to cycle through
colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown' , '#ffc3a0' , '#6dd5ed' , '#753a88']
color_index = 0

marquee()

# Create labels
length_label = tk.Label(app, text="Password Length:", height=3)
length_label.pack(pady=10)

# Create an entry field for the user to input password length
length_entry = tk.Entry(app, width=20)
length_entry.pack()

# Create a button to generate the password
generate_button = tk.Button(app, text="Generate Password", command=generate_password, bg='#ffc3a0', fg='#141e30')
generate_button.pack(pady=10)

# Create an entry field to display the generated password
password_entry = tk.Entry(app, width=50, show='*')
password_entry.pack(pady=10)

# Create a frame to hold the buttons
button_frame = tk.Frame(app)
button_frame.pack()

# Create buttons for other options
copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard, bg='#6dd5ed', fg='#141e30')
copy_button.pack(side=tk.LEFT, padx=10, pady=10)

reset_button = tk.Button(button_frame, text="Reset Password", command=reset_password, bg='#02aab0', fg='#141e30')
reset_button.pack(side=tk.LEFT, padx=10, pady=10)

exit_button = tk.Button(button_frame, text="Exit", command=exit_app, bg='#ffdde1', fg='#141e30')
exit_button.pack(side=tk.LEFT, padx=10, pady=10)

# Create a label to display the generated password
generated_password_label = tk.Label(app, text="Generated Password: ", font=('Helvetica', 12))
generated_password_label.pack(pady=10)

app.mainloop()
