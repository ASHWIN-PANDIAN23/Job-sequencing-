import tkinter as tk
from tkinter import messagebox

class JobSequencing:
    class Job:
        def __init__(self, job_id, deadline, profit):
            self.job_id = job_id
            self.deadline = deadline
            self.profit = profit

    def __init__(self):
        self.jobs = []

    def add_job(self, job_id, deadline, profit):
        job = self.Job(job_id, deadline, profit)
        self.jobs.append(job)

    def schedule_jobs(self):
        if not self.jobs:
            return [], 0
        self.jobs.sort(key=lambda x: x.profit, reverse=True)
        max_deadline = max(job.deadline for job in self.jobs)
        schedule = [-1] * max_deadline
        total_profit = 0
        for job in self.jobs:
            for slot in range(min(max_deadline, job.deadline) - 1, -1, -1):
                if schedule[slot] == -1:
                    schedule[slot] = job.job_id
                    total_profit += job.profit
                    break

        return schedule, total_profit

class JobSequencingUI:
    def __init__(self, root):
        self.scheduler = JobSequencing()

        # Job ID input
        tk.Label(root, text="Job ID").grid(row=0, column=0)
        self.entry_job_id = tk.Entry(root)
        self.entry_job_id.grid(row=0, column=1)

        # Deadline input
        tk.Label(root, text="Deadline").grid(row=1, column=0)
        self.entry_deadline = tk.Entry(root)
        self.entry_deadline.grid(row=1, column=1)

        # Profit input
        tk.Label(root, text="Profit").grid(row=2, column=0)
        self.entry_profit = tk.Entry(root)
        self.entry_profit.grid(row=2, column=1)

        # Add job button
        btn_add_job = tk.Button(root, text="Add Job", command=self.add_job)
        btn_add_job.grid(row=3, column=0, columnspan=2)

        # Listbox to display jobs
        self.listbox_jobs = tk.Listbox(root, height=6, width=50)
        self.listbox_jobs.grid(row=4, column=0, columnspan=2)

        # Calculate sequence button
        btn_calculate = tk.Button(root, text="Calculate Sequence", command=self.calculate_sequence)
        btn_calculate.grid(row=5, column=0, columnspan=2)

        # Result label
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=6, column=0, columnspan=2)

        # Clear jobs button
        btn_clear = tk.Button(root, text="Clear Jobs", command=self.clear_jobs)
        btn_clear.grid(row=7, column=0, columnspan=2)

    def add_job(self):
        job_id = self.entry_job_id.get()
        try:
            deadline = int(self.entry_deadline.get())
            profit = int(self.entry_profit.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for deadline and profit")
            return

        if not job_id or deadline <= 0 or profit < 0:
            messagebox.showerror("Invalid input", "Please provide valid input for all fields")
            return

        # Add job to the scheduler
        self.scheduler.add_job(job_id, deadline, profit)

        # Update listbox
        self.listbox_jobs.insert(tk.END, f"Job ID: {job_id}, Deadline: {deadline}, Profit: {profit}")
        self.entry_job_id.delete(0, tk.END)
        self.entry_deadline.delete(0, tk.END)
        self.entry_profit.delete(0, tk.END)

    def calculate_sequence(self):
        schedule, total_profit = self.scheduler.schedule_jobs()

        if not schedule:
            messagebox.showwarning("No jobs", "Please add jobs first.")
            return

        self.result_label.config(text=f"Scheduled Jobs: {schedule}\nTotal Profit: {total_profit}")

    def clear_jobs(self):
        self.scheduler.jobs.clear()
        self.listbox_jobs.delete(0, tk.END)
        self.result_label.config(text="")

# Main code to run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Job Sequencing Problem")
    app = JobSequencingUI(root)
    root.mainloop()
