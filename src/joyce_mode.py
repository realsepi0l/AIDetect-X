# src/joyce_mode.py

from utils.face_utils import recognize_face_live
from src.phishing_detector import scan_email

def joyce_mode():
    print("🧠 Launching Joyce Face Recognition...")

    user = recognize_face_live()

    if not user:
        print("❌ Intruder Alert!")
        return

    print(f"✅ Welcome, {user}")
    print("Identity Verified. Running Phishing Detection...")

    is_phishing, confidence = scan_email('data/emails/sample_email.txt')
    if is_phishing:
        print(f"⚠ Phising Detected! ( {confidence * 100:.6f}% confidence)")
    else:
        print(f"✅ Email is clean. ( {confidence * 100:.6f}% confidence)")

