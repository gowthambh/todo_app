import os
import json
from datetime import datetime
from tkinter import Tk, Entry, Button, Listbox, StringVar, Scrollbar, Frame, messagebox, simpledialog
from tkinter import ttk
from tkcalendar import DateEntry

TODO_FILE = "todo_data.json"
COMPLETED_FILE = "completed_data.json"

# Custom colors for priority levels
PRIORITY_COLORS = {"High": "red", "Medium": "orange", "Low": "green"}

# Global variable to track the current theme
current_theme = "light"

def load_tasks(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        return []

def save_tasks(file_path, tasks):
    with open(file_path, "w") as file:
        json.dump(tasks, file, indent=2)

def sort_tasks_by_due_date():
    tasks.sort(key=lambda x: datetime.strptime(x['due_date'], "%m/%d/%y"))
    update_task_listbox()

def sort_tasks_by_priority():
    tasks.sort(key=lambda x: x['priority'])
    update_task_listbox()

def toggle_dark_mode():
    global current_theme
    if current_theme == "light":
        root.configure(bg="#2E2E2E", highlightbackground="#2E2E2E")
        button_frame.configure(bg="#2E2E2E")
        listbox_frame.configure(bg="#2E2E2E")
        task_listbox.configure(bg="#2E2E2E", fg="white", selectbackground="black", selectforeground="white")
        completed_listbox.configure(bg="#2E2E2E", fg="white", selectbackground="black", selectforeground="white")
        current_theme = "dark"
    else:
        root.configure(bg="white", highlightbackground="white")
        button_frame.configure(bg="white")
        listbox_frame.configure(bg="white")
        task_listbox.configure(bg="white", fg="black", selectbackground="#E1EFFF", selectforeground="black")
        completed_listbox.configure(bg="white", fg="black", selectbackground="#E1EFFF", selectforeground="black")
        current_theme = "light"

def update_task_listbox():
    task_listbox.delete(0, "end")
    for i, task in enumerate(tasks, start=1):
        status = "Completed" if task['completed'] else "Not Completed"
        task_listbox.insert("end", f"{i}. {task['name']} - {task['description']} - Due: {task['due_date']} - Priority: {task['priority']} - Status: {status}")
        task_listbox.itemconfig(i - 1, {'bg': PRIORITY_COLORS.get(task['priority'], 'white')})

def update_completed_listbox():
    completed_listbox.delete(0, "end")
    for i, task in enumerate(completed_tasks, start=1):
        completed_listbox.insert("end", f"{i}. {task['name']} - {task['description']} - Completed on: {task['completion_date']} {task['completion_time']}")

def add_task():
    name = entry_name.get()
    description = entry_description.get()
    due_date_str = cal.get_date()
    priority = priority_var.get()

    if not name or not description or not due_date_str or not priority:
        result_var.set("Please fill in all fields.")
        return

    if isinstance(due_date_str, datetime):
        due_date_str = due_date_str.strftime("%m/%d/%y")
    else:
        try:
            due_date_obj = datetime.strptime(str(due_date_str), "%Y-%m-%d")
            due_date_str = due_date_obj.strftime("%m/%d/%y")
        except ValueError:
            result_var.set("Invalid due date format.")
            return

    task = {
        "name": name,
        "description": description,
        "due_date": due_date_str,
        "priority": priority,
        "completed": False,
    }
    tasks.append(task)
    save_tasks(TODO_FILE, tasks)
    update_task_listbox()
    result_var.set("Task added!") 

def remove_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        index = int(selected_task_index[0])
        removed_task = tasks.pop(index)
        save_tasks(TODO_FILE, tasks)
        update_task_listbox()
        result_var.set(f"Task '{removed_task['name']}' removed!")
    else:
        result_var.set("Please select a task to remove.")

def mark_completed():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        index = int(selected_task_index[0])
        tasks[index]["completed"] = True
        tasks[index]["completion_date"] = datetime.now().strftime("%m/%d/%y")
        tasks[index]["completion_time"] = datetime.now().strftime("%I:%M %p")
        completed_tasks.append(tasks.pop(index))
        save_tasks(TODO_FILE, tasks)
        save_tasks(COMPLETED_FILE, completed_tasks)
        update_task_listbox()
        update_completed_listbox()
        result_var.set("Task marked as completed!")
    else:
        result_var.set("Please select a task to mark as completed.")

def clear_completed_tasks():
    global completed_tasks
    completed_tasks = []
    save_tasks(COMPLETED_FILE, completed_tasks)
    update_completed_listbox()
    result_var.set("Completed tasks cleared.")

# Load tasks from the file
tasks = load_tasks(TODO_FILE)
completed_tasks = load_tasks(COMPLETED_FILE)

# Create the main window
root = Tk()
root.title("To-Do List")

# Create and set up frames
input_frame = Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
button_frame = Frame(root)
button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")
listbox_frame = Frame(root)
listbox_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="ns")

# Create and set up themed widgets
label_name = ttk.Label(input_frame, text="Task Name:", font=("Helvetica", 12))
entry_name = ttk.Entry(input_frame, font=("Helvetica", 12))
label_description = ttk.Label(input_frame, text="Description:", font=("Helvetica", 12))
entry_description = ttk.Entry(input_frame, font=("Helvetica", 12))
label_due_date = ttk.Label(input_frame, text="Due Date:", font=("Helvetica", 12))
cal = DateEntry(input_frame, width=12, background="darkblue", foreground="white", borderwidth=2)
cal.grid(row=2, column=1, pady=5, padx=10, sticky="w")
label_priority = ttk.Label(input_frame, text="Priority:", font=("Helvetica", 12))
priority_var = ttk.Combobox(input_frame, values=["High", "Medium", "Low"], font=("Helvetica", 12))
priority_var.set("Medium")
button_add = ttk.Button(button_frame, text="Add Task", command=add_task, style="TButton")
button_remove = ttk.Button(button_frame, text="Remove Task", command=remove_task, style="TButton")
button_mark_completed = ttk.Button(button_frame, text="Mark Completed", command=mark_completed, style="TButton")
toggle_dark_mode_button = ttk.Button(button_frame, text="Toggle Dark Mode", command=toggle_dark_mode, style="TButton")
sort_by_due_date_button = ttk.Button(button_frame, text="Sort by Due Date", command=sort_tasks_by_due_date, style="TButton")
sort_by_priority_button = ttk.Button(button_frame, text="Sort by Priority", command=sort_tasks_by_priority, style="TButton")
task_listbox = Listbox(listbox_frame, width=80, height=10, selectmode="single", font=("Helvetica", 12))
scrollbar = Scrollbar(listbox_frame, orient="vertical")
task_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=task_listbox.yview)
completed_listbox = Listbox(listbox_frame, width=80, height=5, selectmode="single", font=("Helvetica", 12))
scrollbar_completed = Scrollbar(listbox_frame, orient="vertical")
completed_listbox.config(yscrollcommand=scrollbar_completed.set)
scrollbar_completed.config(command=completed_listbox.yview)
result_var = StringVar()
label_result = ttk.Label(root, textvariable=result_var, font=("Helvetica", 12))

# Place widgets in the frames
label_name.grid(row=0, column=0, pady=5, sticky="w")
entry_name.grid(row=0, column=1, pady=5, padx=10, sticky="w")
label_description.grid(row=1, column=0, pady=5, sticky="w")
entry_description.grid(row=1, column=1, pady=5, padx=10, sticky="w")
label_due_date.grid(row=2, column=0, pady=5, sticky="w")
label_priority.grid(row=3, column=0, pady=5, sticky="w")
priority_var.grid(row=3, column=1, pady=5, padx=10, sticky="w")
button_add.grid(row=5, column=0, pady=10, sticky="w")
button_remove.grid(row=6, column=0, pady=5, sticky="w")
button_mark_completed.grid(row=7, column=0, pady=5, sticky="w")
toggle_dark_mode_button.grid(row=8, column=0, pady=5, sticky="w")
sort_by_due_date_button.grid(row=9, column=0, pady=5, sticky="w")
sort_by_priority_button.grid(row=10, column=0, pady=5, sticky="w")
button_clear_completed = ttk.Button(button_frame, text="Clear Completed Tasks", command=clear_completed_tasks, style="TButton")
button_clear_completed.grid(row=11, column=0, pady=5, sticky="w")
task_listbox.grid(row=0, column=0, rowspan=3, pady=10, padx=10, sticky="nsew")
scrollbar.grid(row=0, column=1, rowspan=3, sticky="ns", pady=10)
completed_listbox.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")
scrollbar_completed.grid(row=3, column=1, sticky="ns", pady=10)
label_result.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")

# Configure row and column weights for flexibility
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
listbox_frame.columnconfigure(0, weight=1)

# Initialize the task listbox and completed listbox
update_task_listbox()
update_completed_listbox()

# Run the main event loop
root.mainloop()
