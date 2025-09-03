# Examination Software (Starter)

A minimal Python Tkinter app for creating computer-based exams with admin signup/login, QR code generation, 4‑digit OTP, and student attempt saving to text files.

## Features
- **Admin signup/login** (file-based, hashed password).
- **Create exam**: title + questions; saved as `exam.txt` in a unique exam folder under `data/`.
- **QR code** (PNG) is generated for each exam; it encodes a simple URI like `exam://<EXAM_ID>`.
- **4-digit OTP** set by admin per exam (or auto-generated).
- **Student mode**: enter the **Exam Code** (visible when you scan the QR) + OTP to unlock the exam and submit answers.
- **All files** for an exam live together in one folder: `exam.txt`, `exam_qr.png`, `metadata.json`, `student_solution_<name>.txt`.

> Note: This is a starter project focused on local, file-based flows. The QR encodes an exam code, not a URL. When scanning the QR with a phone, you'll see a code like `exam://EXAM_2025...`. Tell students to type the part after `exam://` into **Student Mode → Exam Code** on the computer running this app.

## Tech
- Python 3.9+
- Tkinter for GUI
- `qrcode` + `Pillow` for QR generation
- `bcrypt` for hashing admin password

## Install
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

## Folder Structure
```
exam_app/
  app.py
  auth.py
  exam_manager.py
  requirements.txt
  README.md
  data/                # exam folders are created here
```

## Usage
1. **Run the app** → Choose **Sign up** to create an admin account, then **Log in**.
2. In **Admin Dashboard** → fill Exam Title, Questions, and either set a **4-digit OTP** or click **Generate OTP**.
3. Click **Create Exam** → this creates a folder under `data/<EXAM_ID>/` with:
   - `exam.txt` (the paper),
   - `exam_qr.png` (QR with code `exam://<EXAM_ID>`),
   - `metadata.json` (includes title, OTP, timestamps).
4. Share the QR image. When scanned, it shows the code (e.g., `exam://EXAM_2025_08_29_123456_ABCD`).
5. **Student Mode** → Enter the **Exam Code** (without `exam://`) and the **OTP** to start. After finishing, answers save to `student_solution_<name>.txt` in the same folder.

## Notes
- This is a single-machine starter. Networking/camera decoding are intentionally out-of-scope.
- You can replace the QR content to point to a URL or API later if you move to a client-server design.
- For real deployments, use a secure DB for users/exams and stronger access rules.

## License
MIT
