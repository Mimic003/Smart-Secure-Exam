import tkinter as tk
from tkinter import messagebox, filedialog
from auth import signup, login, is_registered
from exam_manager import create_exam_folder, save_exam_files, find_exam_by_code, save_student_solution
import re
import random

APP_TITLE = "Examination Software (Starter)"

def validate_otp(otp: str) -> bool:
    return bool(re.fullmatch(r"\d{4}", otp))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("820x640")
        self.resizable(True, True)
        self.active_user = None
        self._show_welcome()

    # ---------- Navigation ----------
    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _show_welcome(self):
        self._clear()
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text=APP_TITLE, font=("Segoe UI", 18, "bold")).pack(pady=(0,10))
        tk.Label(frame, text="Select an option to continue").pack(pady=(0,20))

        tk.Button(frame, text="Admin Login", width=20, command=self._show_login).pack(pady=6)
        tk.Button(frame, text="Admin Sign Up", width=20, command=self._show_signup).pack(pady=6)
        tk.Button(frame, text="Student Mode", width=20, command=self._show_student_mode).pack(pady=6)

    # ---------- Auth ----------
    def _show_signup(self):
        self._clear()
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Admin Sign Up", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,10))

        tk.Label(frame, text="Username").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        e_user = tk.Entry(frame, width=30)
        e_user.grid(row=1, column=1, padx=6, pady=6)

        tk.Label(frame, text="Password").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        e_pass = tk.Entry(frame, width=30, show="*")
        e_pass.grid(row=2, column=1, padx=6, pady=6)

        def do_signup():
            u, p = e_user.get().strip(), e_pass.get().strip()
            try:
                signup(u, p)
                messagebox.showinfo("Success", "Admin registered. Please log in.")
                self._show_login()
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        tk.Button(frame, text="Create Admin", command=do_signup).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Back", command=self._show_welcome).grid(row=4, column=0, columnspan=2, pady=4)

    def _show_login(self):
        self._clear()
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Admin Login", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,10))

        tk.Label(frame, text="Username").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        e_user = tk.Entry(frame, width=30)
        e_user.grid(row=1, column=1, padx=6, pady=6)

        tk.Label(frame, text="Password").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        e_pass = tk.Entry(frame, width=30, show="*")
        e_pass.grid(row=2, column=1, padx=6, pady=6)

        def do_login():
            u, p = e_user.get().strip(), e_pass.get().strip()
            try:
                ok = login(u, p)
            except Exception as ex:
                messagebox.showerror("Error", str(ex))
                return
            if ok:
                self.active_user = u
                self._show_admin_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials.")

        tk.Button(frame, text="Login", command=do_login).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Back", command=self._show_welcome).grid(row=4, column=0, columnspan=2, pady=4)

    # ---------- Admin Dashboard ----------
    def _show_admin_dashboard(self):
        self._clear()
        frame = tk.Frame(self, padx=16, pady=16)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=f"Welcome, {self.active_user}", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,10))

        form = tk.Frame(frame)
        form.pack(fill="x", pady=10)

        # Title
        tk.Label(form, text="Exam Title").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        e_title = tk.Entry(form, width=50)
        e_title.grid(row=0, column=1, padx=6, pady=6, sticky="w")

        # OTP
        tk.Label(form, text="4-digit OTP").grid(row=0, column=2, sticky="e", padx=6, pady=6)
        e_otp = tk.Entry(form, width=10)
        e_otp.grid(row=0, column=3, padx=6, pady=6, sticky="w")

        def gen_otp():
            e_otp.delete(0, tk.END)
            e_otp.insert(0, f"{random.randint(0,9999):04d}")
        tk.Button(form, text="Generate OTP", command=gen_otp).grid(row=0, column=4, padx=6, pady=6)

        # Questions
        tk.Label(form, text="Questions (one per line or paragraphs)").grid(row=1, column=0, sticky="ne", padx=6, pady=6)
        t_questions = tk.Text(form, width=80, height=20)
        t_questions.grid(row=1, column=1, columnspan=4, padx=6, pady=6, sticky="w")

        def create_exam():
            title = e_title.get().strip()
            otp = e_otp.get().strip()
            questions = t_questions.get("1.0", tk.END).strip()
            if not title:
                messagebox.showerror("Error", "Please enter an exam title.")
                return
            if not validate_otp(otp):
                messagebox.showerror("Error", "OTP must be exactly 4 digits.")
                return
            if not questions:
                messagebox.showerror("Error", "Please enter questions/content.")
                return

            folder, exam_id = create_exam_folder(title)
            qr_path = save_exam_files(folder, exam_id, title, questions, otp)
            messagebox.showinfo("Exam Created",
                                f"Exam ID: {exam_id}\n\nFolder:\n{folder}\n\nQR saved as:\n{qr_path}")

        tk.Button(frame, text="Create Exam", command=create_exam).pack(pady=8)
        tk.Button(frame, text="Logout", command=self._show_welcome).pack(pady=4)

    # ---------- Student Mode ----------
    def _show_student_mode(self):
        self._clear()
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Student Mode", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0,10))

        form = tk.Frame(frame)
        form.pack(anchor="w")

        tk.Label(form, text="Your Name").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        e_name = tk.Entry(form, width=40)
        e_name.grid(row=0, column=1, padx=6, pady=6, sticky="w")

        tk.Label(form, text="Exam Code").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        e_code = tk.Entry(form, width=40)
        e_code.grid(row=1, column=1, padx=6, pady=6, sticky="w")
        tk.Label(form, text="(Type the code shown after scanning the QR; exclude 'exam://')").grid(row=1, column=2, padx=6, pady=6, sticky="w")

        tk.Label(form, text="OTP (4 digits)").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        e_otp = tk.Entry(form, width=10)
        e_otp.grid(row=2, column=1, sticky="w", padx=6, pady=6)

        # Placeholder for loaded exam content
        t_exam = tk.Text(frame, width=100, height=18, state="disabled")
        t_exam.pack(pady=10, fill="both", expand=True)

        def unlock_exam():
            name = e_name.get().strip()
            exam_code = e_code.get().strip()
            otp = e_otp.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter your name.")
                return
            if not exam_code:
                messagebox.showerror("Error", "Please enter the exam code.")
                return
            if not re.fullmatch(r"\d{4}", otp or ""):
                messagebox.showerror("Error", "OTP must be exactly 4 digits.")
                return

            meta, exam_dir = find_exam_by_code(exam_code)
            if not meta:
                messagebox.showerror("Error", "Exam not found. Check the code with your invigilator.")
                return
            if meta.get("otp") != otp:
                messagebox.showerror("Error", "Incorrect OTP. Please try again.")
                return

            # Load and show exam.txt
            try:
                with open(f"{exam_dir}/exam.txt", "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as ex:
                messagebox.showerror("Error", f"Failed to load exam: {ex}")
                return

            t_exam.config(state="normal")
            t_exam.delete("1.0", tk.END)
            t_exam.insert("1.0", content + "\n\n--- Write your answers below this line ---\n")
            t_exam.config(state="normal")

            # Save button appears after unlock
            def save_solution():
                answers = t_exam.get("1.0", tk.END).strip()
                try:
                    path = save_student_solution(exam_dir, name, answers)
                except Exception as ex:
                    messagebox.showerror("Error", f"Could not save solution: {ex}")
                    return
                messagebox.showinfo("Saved", f"Your answers have been saved to:\n{path}")

            tk.Button(frame, text="Submit Answers", command=save_solution).pack(pady=6)

        tk.Button(frame, text="Unlock Exam", command=unlock_exam).pack(pady=8)
        tk.Button(frame, text="Back", command=self._show_welcome).pack(pady=4)

if __name__ == "__main__":
    App().mainloop()
