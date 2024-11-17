from tkinter import messagebox
from ttkbootstrap import Style
from ttkbootstrap.widgets import *
from task_logic import TaskLogic


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("400x600")
        self.root.iconbitmap("DALL·E-2024-11-15-09.38.ico")

        style = Style(theme="superhero")  # Choose a theme

        # Task Logic instance
        self.logic = TaskLogic()

        # Instruction Label
        self.instruction_label = tk.Label(self.root, text="Enter a task below:", font=("Helvetica", 14), bg="#2c3e50", fg="white")
        self.instruction_label.pack(pady=(10, 0))

        # Task Entry Widget
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(pady=10)
        self.task_entry = ttk.Entry(self.entry_frame, width=35, font=("Helvetica", 12))
        self.task_entry.pack()

        # Priority Dropdown
        self.priority_var = tk.StringVar(value="Medium")  # Default priority
        self.priority_label = tk.Label(self.root, text="Select Priority:", font=("Helvetica", 10), bg="#2c3e50",
                                       fg="white")
        self.priority_label.pack(pady=(5, 0))

        self.priority_dropdown = ttk.Combobox(self.root, textvariable=self.priority_var,
                                              values=["High", "Medium", "Low"], state="readonly", width=15)
        self.priority_dropdown.pack(pady=(5, 10))

        # Button Frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        # Buttons
        self.add_button = ttk.Button(self.button_frame, text="Add Task", style="success", width=12, command=self.add_task)
        self.add_button.grid(row=0, column=0, padx=5)

        self.delete_button = ttk.Button(self.button_frame, text="Delete Task", style="danger", width=12, command=self.delete_task)
        self.delete_button.grid(row=0, column=1, padx=5)

        self.clear_button = ttk.Button(self.button_frame, text="Clear All", style="primary", width=12, command=self.clear_all_tasks)
        self.clear_button.grid(row=0, column=2, padx=5)

        self.complete_button = ttk.Button(self.button_frame, text="Mark Complete", style="info", width=12, command=self.toggle_completion)
        self.complete_button.grid(row=1, column=0, padx=5, pady=(5, 0))

        self.edit_button = ttk.Button(self.button_frame, text="Edit Task", style="warning", width=12, command=self.edit_task)
        self.edit_button.grid(row=1, column=1, padx=5, pady=(5, 0))

        self.cancel_edit_button = ttk.Button(self.button_frame, text="Cancel Edit", style="secondary", width=12, command=self.cancel_edit)
        self.cancel_edit_button.grid(row=1, column=2, padx=5, pady=(5, 0))

        # Exit Button
        self.exit_button = ttk.Button(self.button_frame, text="Exit", style="danger", width=12, command=self.on_exit)
        self.exit_button.grid(row=2, column=0, padx=5, pady=(5, 0))  # Adds some padding for spacing

        # Bind the window close button to prompt for saving tasks
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Listbox with Scrollbar Integration
        self.listbox_frame = tk.Frame(self.root, bg="#e0f7fa", bd=0, relief="solid")
        self.listbox_frame.place(relx=0.5, rely=0.73, anchor="center", width=250, height=300)

        self.task_listbox = tk.Listbox(
            self.listbox_frame, font=("Helvetica", 12), selectmode=tk.SINGLE, height=12, width=20, bd=0, highlightthickness=0, bg="#f0f0f0"
        )
        self.task_listbox.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.listbox_frame, orient="vertical", command=self.task_listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure Listbox to work with Scrollbar
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        # Grid Configuration for proper expansion
        self.listbox_frame.grid_rowconfigure(0, weight=1)
        self.listbox_frame.grid_columnconfigure(0, weight=1)

        # Setup for saving and loading tasks
        self.load_tasks()  # Load tasks when the app starts


    # Function to add a task
    def add_task(self):
        self.logic.add_task(self.task_entry, self.task_listbox, self.priority_var)

    # Function to delete a selected task
    def delete_task(self):
        self.logic.delete_task(self.task_listbox)

    # Function to clear all tasks
    def clear_all_tasks(self):
        self.logic.clear_all_tasks(self.task_listbox)

    # Function to toggle task completion
    def toggle_completion(self):
        self.logic.toggle_task_completion(self.task_listbox)

    def edit_task(self):
        self.logic.edit_task(self.task_entry, self.task_listbox)

    def cancel_edit(self):
        self.logic.cancel_edit(self.task_listbox, self.task_entry)

    # Save tasks to a file
    def save_tasks(self):
        self.logic.save_tasks(self.task_listbox)

    # Load tasks from a file
    def load_tasks(self):
        self.logic.load_tasks(self.task_listbox)

    # Prompt for saving tasks on exit
    def on_exit(self):
        # Check if there are any tasks in the Listbox
        if self.task_listbox.size() > 0:  # Only prompt if there are tasks
            if messagebox.askyesno("Exit", "Do you want to save your tasks before exiting?"):
                self.save_tasks()
        self.root.destroy()  # Close the app


