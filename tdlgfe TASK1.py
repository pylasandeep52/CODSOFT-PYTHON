import tkinter as tk
from tkinter import messagebox
import json

def marquee():
    global marquee_offset, color_index
    canvas.coords(text_id, marquee_offset, 10)
    marquee_offset -= 1
    if marquee_offset <= -marquee_text_width:
        marquee_offset = window_width
    canvas.itemconfig(text_id, fill=colors[color_index])  # Change text color
    color_index = (color_index + 1) % len(colors)  # Move to the next color
    canvas.after(3, marquee)  # Update every 3 milliseconds


def load_data(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return []

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

def display_tasks():
    listbox_tasks.delete(0, tk.END)
    if not tasks:
        listbox_tasks.insert(tk.END, "No tasks found. Add some tasks to your TO-DO-LIST.")
    else:
        for index, task in enumerate(tasks, start=1):
            status_icon = "✔" if task['status'] == 'Completed' else " "
            description = task.get('description', 'N/A')
            due_date = task.get('due_date', 'N/A')
            priority = task.get('priority', 'N/A')
            listbox_tasks.insert(tk.END, f"{index}. [{status_icon}] {description} (Due: {due_date}, Priority: {priority})")

def create_task():
    description = entry_task.get()
    due_date = entry_date.get()
    priority = entry_priority.get()

    if description:
        task = {
            'description': description,
            'due_date': due_date,
            'priority': priority,
            'status': 'Incomplete'
        }
        tasks.append(task)
        save_data(filename, tasks)
        display_tasks()
        entry_task.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        entry_priority.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task description.")

def update_task():
    selected_task_index = listbox_tasks.curselection()
    if selected_task_index:
        task_index = int(selected_task_index[0])
        new_description = entry_task.get()
        due_date = entry_date.get()
        priority = entry_priority.get()

        if new_description:
            tasks[task_index]['description'] = new_description
            tasks[task_index]['due_date'] = due_date
            tasks[task_index]['priority'] = priority
            save_data(filename, tasks)
            display_tasks()
            entry_task.delete(0, tk.END)
            entry_date.delete(0, tk.END)
            entry_priority.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task description.")

def mark_task_as_completed():
    selected_task_index = listbox_tasks.curselection()
    if selected_task_index:
        task_index = int(selected_task_index[0])
        tasks[task_index]['status'] = 'Completed'
        save_data(filename, tasks)
        display_tasks()

def delete_task():
    selected_task_index = listbox_tasks.curselection()
    if selected_task_index:
        task_index = int(selected_task_index[0])
        del tasks[task_index]
        save_data(filename, tasks)
        display_tasks()

def sort_by_due_date():
    tasks.sort(key=lambda task: task.get('due_date', ''))
    display_tasks()

def sort_by_priority():
    tasks.sort(key=lambda task: task.get('priority', ''))
    display_tasks()


# Initialize the main window
app = tk.Tk()
app.title("TO-DO-LIST Application")
app.geometry("500x400")
app.configure(bg='lightgray')  # Set background color for the main window


filename = "todo_data.json"
tasks = load_data(filename)



marquee_text = "TO-DO-LIST application"
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



# Styling for labels and buttons
label_task = tk.Label(app, text="Task Description:", bg='lightgray', font=('Helvetica', 12))
label_task.pack(pady=5)  # Add vertical spacing




entry_task = tk.Entry(app, width=50, font=('Helvetica', 12))
entry_task.pack(pady=5)  # Add vertical spacing



label_date = tk.Label(app, text="Due Date:", bg='lightgray', font=('Helvetica', 12))
label_date.pack(pady=5)  # Add vertical spacing

entry_date = tk.Entry(app, width=50, font=('Helvetica', 12))
entry_date.pack(pady=5)  # Add vertical spacing

label_priority = tk.Label(app, text="Priority:", bg='lightgray', font=('Helvetica', 12))
label_priority.pack(pady=5)  # Add vertical spacing

entry_priority = tk.Entry(app, width=50, font=('Helvetica', 12))
entry_priority.pack(pady=5)  # Add vertical spacing

button_add_task = tk.Button(app, text="Add Task", command=create_task, bg='#2c3e50', fg='white', font=('Helvetica', 12))
button_add_task.pack(pady=5, padx=10)  # Add vertical and horizontal spacing

listbox_tasks = tk.Listbox(app, height=10, width=60, selectmode=tk.SINGLE, bg='white', bd=1, font=('Helvetica', 12))
listbox_tasks.pack(pady=10)  # Add vertical spacing



button_update_task = tk.Button(app, text="Update Task", command=update_task, bg='#ffc3a0', fg='#141e30', font=('Helvetica', 12) , bd=1)
button_update_task.pack(side=tk.LEFT, padx=100, pady=5)  # Add vertical and horizontal spacing

button_mark_completed = tk.Button(app, text="Mark as Completed", command=mark_task_as_completed, bg='#6dd5ed', fg='#141e30', font=('Helvetica', 12))
button_mark_completed.pack(side=tk.LEFT, padx=70, pady=5 )  # Add vertical and horizontal spacing

button_delete_task = tk.Button(app, text="Delete Task", command=delete_task, bg='#753a88', fg='#141e30', font=('Helvetica', 12))
button_delete_task.pack(side=tk.LEFT, padx=60,pady=5)  # Add vertical and horizontal spacing

button_sort_by_due_date = tk.Button(app, text="Sort by Due Date", command=sort_by_due_date, bg='#ffdde1', fg='#141e30', font=('Helvetica', 12))
button_sort_by_due_date.pack(side=tk.LEFT, padx=60, pady=5)  # Add vertical and horizontal spacing

button_sort_by_priority = tk.Button(app, text="Sort by Priority", command=sort_by_priority, bg='#02aab0', fg='#141e30', font=('Helvetica', 12))
button_sort_by_priority.pack(side=tk.LEFT, padx=60, pady=5)  # Add vertical and horizontal spacing

display_tasks()

app.mainloop()

