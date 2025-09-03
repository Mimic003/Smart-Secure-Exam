import os
import re
import json
import datetime
import qrcode

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def _slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_") or "exam"

def create_exam_folder(title: str) -> str:
    os.makedirs(DATA_DIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
    exam_id = f"EXAM_{ts}_{_slugify(title)[:20]}"
    folder = os.path.join(DATA_DIR, exam_id)
    os.makedirs(folder, exist_ok=True)
    return folder, exam_id

def save_exam_files(folder: str, exam_id: str, title: str, questions: str, otp: str):
    # Save exam text
    exam_txt = os.path.join(folder, "exam.txt")
    with open(exam_txt, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\nExam ID: {exam_id}\n\nQuestions:\n{questions}\n")

    # Metadata
    meta = {
        "exam_id": exam_id,
        "title": title,
        "otp": otp,
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    with open(os.path.join(folder, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    # QR code (encodes exam://<EXAM_ID>)
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(f"exam://{exam_id}")
    qr.make(fit=True)
    img = qr.make_image()
    qr_path = os.path.join(folder, "exam_qr.png")
    img.save(qr_path)
    return qr_path

def find_exam_by_code(exam_code: str):
    exam_dir = os.path.join(DATA_DIR, exam_code)
    meta_path = os.path.join(exam_dir, "metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f), exam_dir
    return None, None

def save_student_solution(exam_dir: str, student_name: str, answers: str):
    safe_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", student_name.strip()) or "student"
    path = os.path.join(exam_dir, f"student_solution_{safe_name}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(answers)
    return path
