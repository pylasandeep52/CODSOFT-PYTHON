import tkinter as tk



def marquee():
    global marquee_offset, color_index
    canvas.coords(text_id, marquee_offset, 10)
    marquee_offset -= 1
    if marquee_offset <= -marquee_text_width:
        marquee_offset = window_width
    canvas.itemconfig(text_id, fill=colors[color_index])  # Change text color
    color_index = (color_index + 1) % len(colors)  # Move to the next color
    canvas.after(3, marquee)  # Update every 3 milliseconds

def clear():
    entry_var.set("")

def evaluate():
    try:
        result = eval(entry_var.get())
        entry_var.set(result)
    except:
        entry_var.set("Error")

def append_to_display(value):
    current_text = entry_var.get()
    entry_var.set(current_text + str(value))

# Initialize the main window
app = tk.Tk()
app.title("Mobile Calculator")
app.geometry("500x400")
app.configure(bg='#F0F0F0')

marquee_text = "Simple Calculator application"
canvas = tk.Canvas(app, width=1500, height=28)
canvas.pack(pady=10)

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



# Entry widget to display the result
entry_var = tk.StringVar()
entry_var.set("")
display = tk.Entry(app, textvariable=entry_var, font=('Helvetica', 20), bd=0, relief=tk.FLAT, justify=tk.RIGHT)
display.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Frame to hold the buttons
button_frame = tk.Frame(app, bg='#F0F0F0')
button_frame.pack(fill=tk.BOTH, expand=True)

# Buttons
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2),
]

for text, row, col in buttons:
    button = tk.Button(button_frame, text=text, font=('Helvetica', 18), bg='lightgray', bd=0, relief=tk.FLAT,
                       command=lambda value=text: append_to_display(value) if value != '=' else evaluate())
    button.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

# Additional buttons
clear_button = tk.Button(button_frame, text='C', font=('Helvetica', 18), bg='lightgray', bd=0, relief=tk.FLAT, command=clear)
clear_button.grid(row=1, column=3, padx=10, pady=10, sticky='nsew')

add_button = tk.Button(button_frame, text='+', font=('Helvetica', 18), bg='lightgray', bd=0, relief=tk.FLAT,
                       command=lambda value='+': append_to_display(value))
add_button.grid(row=2, column=3, padx=10, pady=10, sticky='nsew')

subtract_button = tk.Button(button_frame, text='-', font=('Helvetica', 18), bg='lightgray', bd=0, relief=tk.FLAT,
                            command=lambda value='-': append_to_display(value))
subtract_button.grid(row=3, column=3, padx=10, pady=10, sticky='nsew')

multiply_button = tk.Button(button_frame, text='*', font=('Helvetica', 18), bg='lightgray', bd=0, relief=tk.FLAT,
                            command=lambda value='*': append_to_display(value))
multiply_button.grid(row=4, column=3, padx=10, pady=10, sticky='nsew')

divide_button = tk.Button(button_frame, text='/', font=('Helvetica', 18), bg='lightgray', bd=0, relief=tk.FLAT,
                          command=lambda value='/': append_to_display(value))
divide_button.grid(row=5, column=3, padx=10, pady=10, sticky='nsew')

# Set row and column weights for resizing
for i in range(5):
    button_frame.grid_rowconfigure(i, weight=1)
    button_frame.grid_columnconfigure(i, weight=1)

app.mainloop()
