import tkinter as tk
from tkinter import messagebox
import json
import os

# File to store tasks
TASKS_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        
        self.tasks = load_tasks()
        
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)
        
        self.task_listbox = tk.Listbox(self.frame, width=50, height=10)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.task_listbox.bind("<Double-1>", self.toggle_task)
        
        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)
        
        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=5)
        
        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)
        
        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)
        
        self.update_tasks()

    def update_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "[Done] " if task["completed"] else "[ ] "
            self.task_listbox.insert(tk.END, status + task["task"])

    def add_task(self):
        task_text = self.entry.get()
        if task_text:
            self.tasks.append({"task": task_text, "completed": False})
            save_tasks(self.tasks)
            self.entry.delete(0, tk.END)
            self.update_tasks()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty.")

    def toggle_task(self, event):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]
            save_tasks(self.tasks)
            self.update_tasks()

    def delete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            self.tasks.pop(index)
            save_tasks(self.tasks)
            self.update_tasks()
        else:
            messagebox.showwarning("Warning", "Select a task to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
