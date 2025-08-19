import tkinter as tk
from tkinter import ttk
import datetime
import time

class TaskTimer:
    """Manages the state of a single task timer."""
    def __init__(self, task_name):
        self.task_name = task_name
        self.start_time = None
        self.end_time = None
        self.duration = None

    @property
    def status(self):
        """Returns the current status of the timer."""
        if self.start_time is None:
            return "Not Started"
        elif self.end_time is None:
            return "Running"
        else:
            return "Stopped"

    def start(self):
        """Starts the timer. Returns True if successful, False otherwise."""
        if self.status != "Not Started":
            return False
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.duration = None
        return True

    def stop(self):
        """Stops the timer. Returns True if successful, False otherwise."""
        if self.status != "Running":
            return False
        self.end_time = datetime.datetime.now()
        self.duration = self.end_time - self.start_time
        return True

    def get_duration(self):
        """Gets the duration of the task. Returns current duration if running."""
        if self.duration is None:
            if self.status == "Running":
                return datetime.datetime.now() - self.start_time
            return datetime.timedelta(0)
        else:
            return self.duration

    def reset(self):
        """Resets the timer to its initial state."""
        self.start_time = None
        self.end_time = None
        self.duration = None
        return True

class TaskTimerApp(tk.Tk):
    """Main application class for the Task Timer GUI."""
    def __init__(self):
        super().__init__()
        self.title("Task Timer")
        self.geometry("500x400")

        self.tasks = {}  # {task_name: {'timer': TaskTimer, 'widgets': {}}}

        # --- UI Setup ---
        # Use a themed style
        style = ttk.Style(self)
        style.theme_use('clam')

        # Frame for adding new tasks
        add_task_frame = ttk.Frame(self, padding="10")
        add_task_frame.pack(fill=tk.X)

        self.task_name_entry = ttk.Entry(add_task_frame, width=40)
        self.task_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.task_name_entry.insert(0, "Enter new task name")
        self.task_name_entry.bind("<Return>", self.add_task_event)

        add_button = ttk.Button(add_task_frame, text="Add Task", command=self.add_task)
        add_button.pack(side=tk.LEFT)

        # Separator
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=5)

        # Frame for the list of tasks
        self.tasks_frame = ttk.Frame(self, padding="10")
        self.tasks_frame.pack(fill=tk.BOTH, expand=True)

        # Start the timer update loop
        self.update_display()

    def add_task_event(self, event=None):
        """Callback for entry box <Return> key."""
        self.add_task()

    def add_task(self):
        """Adds a new task to the application."""
        task_name = self.task_name_entry.get().strip()
        if not task_name:
            return
        if task_name in self.tasks:
            print(f"Task '{task_name}' already exists.")
            return

        new_task_timer = TaskTimer(task_name)
        self.tasks[task_name] = {'timer': new_task_timer, 'widgets': {}}

        # Create UI elements for the new task
        task_row_frame = ttk.Frame(self.tasks_frame, padding="5", relief="groove", borderwidth=1)
        task_row_frame.pack(fill=tk.X, pady=2)

        task_label = ttk.Label(task_row_frame, text=task_name, width=20, anchor="w")
        task_label.pack(side=tk.LEFT, padx=(0, 10))

        duration_label = ttk.Label(task_row_frame, text="00:00:00", width=10, anchor="e")
        duration_label.pack(side=tk.LEFT, padx=(0, 10))

        start_button = ttk.Button(task_row_frame, text="Start", command=lambda: self.start_task(task_name))
        start_button.pack(side=tk.LEFT, padx=(0, 5))

        stop_button = ttk.Button(task_row_frame, text="Stop", command=lambda: self.stop_task(task_name))
        stop_button.pack(side=tk.LEFT, padx=(0, 5))

        reset_button = ttk.Button(task_row_frame, text="Reset", command=lambda: self.reset_task(task_name))
        reset_button.pack(side=tk.LEFT)

        self.tasks[task_name]['widgets'] = {
            'frame': task_row_frame,
            'label': task_label,
            'duration_label': duration_label,
            'start_button': start_button,
            'stop_button': stop_button,
            'reset_button': reset_button
        }
        self.task_name_entry.delete(0, tk.END)
        self.task_name_entry.insert(0, "Enter new task name") # Reset placeholder

    def start_task(self, task_name):
        """Starts the timer for the given task."""
        timer = self.tasks[task_name]['timer']
        if timer.start():
            print(f"Started task: {task_name}")
            self.update_button_states(task_name)

    def stop_task(self, task_name):
        """Stops the timer for the given task."""
        timer = self.tasks[task_name]['timer']
        if timer.stop():
            print(f"Stopped task: {task_name}")
            self.update_button_states(task_name)

    def reset_task(self, task_name):
        """Resets the timer for the given task."""
        timer = self.tasks[task_name]['timer']
        if timer.reset():
            print(f"Reset task: {task_name}")
            self.update_button_states(task_name)
            self.tasks[task_name]['widgets']['duration_label'].config(text="00:00:00")

    def update_display(self):
        """Updates the duration display for all running tasks."""
        for task_name, data in self.tasks.items():
            timer = data['timer']
            duration_label = data['widgets']['duration_label']
            if timer.status == "Running":
                duration = timer.get_duration()
                hours, remainder = divmod(duration.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                duration_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
                duration_label.config(text=duration_str)
            self.update_button_states(task_name) # Ensure button states are correct
        self.after(1000, self.update_display) # Call itself every 1 second

    def update_button_states(self, task_name):
        """Updates the enabled/disabled state of buttons based on task status."""
        timer = self.tasks[task_name]['timer']
        widgets = self.tasks[task_name]['widgets']

        if timer.status == "Not Started":
            widgets['start_button'].config(state=tk.NORMAL)
            widgets['stop_button'].config(state=tk.DISABLED)
            widgets['reset_button'].config(state=tk.DISABLED)
        elif timer.status == "Running":
            widgets['start_button'].config(state=tk.DISABLED)
            widgets['stop_button'].config(state=tk.NORMAL)
            widgets['reset_button'].config(state=tk.DISABLED)
        elif timer.status == "Stopped":
            widgets['start_button'].config(state=tk.NORMAL)
            widgets['stop_button'].config(state=tk.DISABLED)
            widgets['reset_button'].config(state=tk.NORMAL)


if __name__ == "__main__":
    app = TaskTimerApp()
    app.mainloop()