import os
import pickle
import face_recognition
import cv2
import pyttsx3
import numpy as np
from datetime import datetime
import time

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def load_face_encodings(file='models/face_encodings.pkl'):
    with open(file, 'rb') as f:
        return pickle.load(f)

def recognize_face_live():
    data = load_face_encodings()
    known_encodings = data["encodings"]
    known_names = data["names"]

    if not known_encodings:
        print("No known face encodings found.")
        return None

    cap = cv2.VideoCapture(0)
    print("Webcam Started. Press 'q' to quit.")

    authorized_user = None
    last_intruder_time = 0
    intruder_cooldown = 10

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, faces)

        for (top, right, bottom, left), encoding in zip(faces, encodings):
            face_distances = face_recognition.face_distance(known_encodings, encoding)
            best_match_index = np.argmin(face_distances)

            name = "Unknown"

            if face_distances[best_match_index] < 0.45:
                name = known_names[best_match_index]
                color = (0, 255, 0)  # Green
                authorized_user = name
                label = f"✅ {name}"
            else:
                label = "❌ Intruder"
                color = (0, 0, 255)

                current_time = time.time()
                if current_time - last_intruder_time > intruder_cooldown:
                    last_intruder_time = current_time

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    intruder_dir = "logs/intruder"
                    os.makedirs(intruder_dir, exist_ok=True)
                    intruder_path = os.path.join(intruder_dir, f"intruder_{timestamp}.jpg")
                    cv2.imwrite(intruder_path, frame)

                    speak("Intruder alert. Snapshot saved.")
                    print(f"[⚠] Intruder snapshot saved at: {intruder_path}")

            # Draw label
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 20), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, label, (left + 5, bottom - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow("Joyce Mode - Face Scan", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if authorized_user:
            speak(f"Welcome, {authorized_user}")
            cap.release()
            cv2.destroyAllWindows()
            return authorized_user

    cap.release()
    cv2.destroyAllWindows()
    return None

