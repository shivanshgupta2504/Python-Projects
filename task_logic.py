from tkinter import messagebox
import json


class TaskLogic:
    def __init__(self):
        self.original_task = None
        self.original_task_index = None
        self.original_task_priority = None  # Store the priority for color restoration

    def add_task(self, task_entry, task_listbox, priority_var):
        task = task_entry.get().strip()
        priority = priority_var.get()
        if task:
            task_number = task_listbox.size() + 1  # Determine the next task number
            task_with_priority = f"{task_number}. [{priority}] {task}"

            # Insert the task with priority
            task_listbox.insert("end", task_with_priority)

            # Color code based on priority
            self.apply_priority_color(task_listbox, "end", priority)

            task_entry.delete(0, "end")  # Clear entry after adding task
        else:
            messagebox.showerror("Task Entry Error", "Task Entry Field is Empty. Please enter a task.")

    def delete_task(self, task_listbox):
        try:
            selected_task_index = task_listbox.curselection()
            if selected_task_index:
                task_listbox.delete(selected_task_index)
                self.renumber_tasks(task_listbox)
            else:
                messagebox.showwarning("Task Selection", "No Task Selected. Please select a task to delete.")
        except Exception as e:
            print(f"Error: {e}")

    def clear_all_tasks(self, task_listbox):
        if task_listbox.size() == 0:
            messagebox.showinfo("Clear All", "No tasks to clear!")
        else:
            confirm = messagebox.askyesno("Clear All", "Are you sure you want to clear all tasks?")
            if confirm:
                task_listbox.delete(0, "end")
                messagebox.showinfo("Clear All", "All tasks have been cleared!")

    def renumber_tasks(self, task_listbox):
        tasks = task_listbox.get(0, "end")
        task_listbox.delete(0, "end")  # Clear the Listbox

        # Re-insert tasks with updated numbering and reapply color coding
        for i, task in enumerate(tasks, start=1):
            # Extract priority from the task to apply the correct color
            priority_start = task.find("[") + 1
            priority_end = task.find("]")
            priority = task[priority_start:priority_end]

            # Extract the task content without the numbering
            task_content = task.split('] ', 1)[1] if "] " in task else task.split('. ', 1)[1]
            updated_task = f"{i}. [{priority}] {task_content}"

            # Insert the updated task
            task_listbox.insert("end", updated_task)

            # Apply the color based on priority
            self.apply_priority_color(task_listbox, i - 1, priority)

    def toggle_task_completion(self, task_listbox):
        selected_task_index = task_listbox.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            task = task_listbox.get(index)

            # Check if task is marked as completed
            if task.startswith("[X] "):  # Already completed
                task_content = task[4:]  # Remove "[X] " prefix
                task_listbox.delete(index)
                task_listbox.insert(index, task_content)
            else:
                task_listbox.delete(index)
                task_listbox.insert(index, f"[X] {task}")  # Mark as completed
        else:
            messagebox.showwarning("Task Selection", "No Task Selected. Please select a task to mark as completed.")

    def edit_task(self, task_entry, task_listbox):
        selected_task_index = task_listbox.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            task = task_listbox.get(index)

            # Save the original task data to restore it if editing is canceled
            self.original_task = task
            self.original_task_index = index

            # Extract the priority for color restoration
            priority_start = task.find("[") + 1
            priority_end = task.find("]")
            self.original_task_priority = task[priority_start:priority_end]

            # Extract only the task content for editing (remove index and priority)
            task_content = task.split('] ', 1)[1] if "] " in task else task.split('. ', 1)[1]

            # Populate the entry field for editing
            task_entry.delete(0, "end")
            task_entry.insert(0, task_content)

            # Temporarily remove the task from the Listbox
            task_listbox.delete(index)
        else:
            messagebox.showwarning("Task Selection", "No Task Selected. Please select a task to edit.")

    def cancel_edit(self, task_listbox, task_entry):
        # Restore the original task if editing is canceled
        if self.original_task is not None and self.original_task_index is not None:
            task_entry.delete(0, "end")
            task_listbox.insert(self.original_task_index, self.original_task)
            self.apply_priority_color(task_listbox, self.original_task_index, self.original_task_priority)

            # Clear the stored original task data after restoring
            self.original_task = None
            self.original_task_index = None
            self.original_task_priority = None

    def apply_priority_color(self, task_listbox, index, priority):
        """Applies the color based on priority."""
        if priority == "High":
            task_listbox.itemconfig(index, {"fg": "red"})
        elif priority == "Medium":
            task_listbox.itemconfig(index, {"fg": "orange"})
        elif priority == "Low":
            task_listbox.itemconfig(index, {"fg": "green"})

    def save_tasks(self, task_listbox, filename="tasks.txt"):
        tasks = task_listbox.get(0, "end")
        tasks_to_save = []

        for task in tasks:
            if not task.startswith("[X] "):  # Only save non-completed tasks
                priority_start = task.find("[") + 1
                priority_end = task.find("]")
                priority = task[priority_start:priority_end]
                task_content = task.split('] ', 1)[1] if "] " in task else task.split('. ', 1)[1]

                tasks_to_save.append({"priority": priority, "task": task_content})

        with open(filename, "w") as f:
            json.dump(tasks_to_save, f)

    def load_tasks(self, task_listbox, filename="tasks.txt"):
        try:
            with open(filename, "r") as f:
                tasks_to_load = json.load(f)

            task_listbox.delete(0, "end")  # Clear current tasks

            for i, task_data in enumerate(tasks_to_load, start=1):
                task_content = task_data["task"]
                priority = task_data["priority"]
                formatted_task = f"{i}. [{priority}] {task_content}"

                task_listbox.insert("end", formatted_task)
                self.apply_priority_color(task_listbox, i - 1, priority)

        except FileNotFoundError:
            messagebox.showinfo("Load Tasks", "No saved tasks found.")
