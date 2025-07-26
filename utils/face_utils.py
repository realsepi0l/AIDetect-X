
import os
import pickle
import face_recognition
import cv2
import pyttsx3
from datetime import datetime
import subprocess

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def encode_known_faces(folder='data/faces/known', output_file='models/face_encodings.pkl'):
    known_encodings = []
    known_names = []

    for filename in os.listdir(folder):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            path = os.path.join(folder, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                name = os.path.splitext(filename)[0]
                known_names.append(name)
                print(f"[+] Encoded: {filename}")
            else:
                print(f"[!] No face found in {filename}")

    data = {"encodings": known_encodings, "names": known_names}
    with open(output_file, "wb") as f:
        pickle.dump(data, f)
        print(f"[✅] Encodings saved to {output_file}")

def load_face_encodings(file='models/face_encodings.pkl'):
    with open(file, 'rb') as f:
        return pickle.load(f)

def log_intruder_snapshot(frame):
    if not os.path.exists("logs/intruders"):
        os.makedirs("logs/intruders")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/intruders/intruder_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"[⚠️] Intruder snapshot saved: {filename}")

def recognize_face_live():
    data = load_face_encodings('models/face_encodings.pkl')
    known_encodings = data["encodings"]
    known_names = data["names"]

    if not known_encodings:
        print("No known face encodings found.")
        return None

    cap = cv2.VideoCapture(0)
    print("Webcam Started. Press 'q' to quit.")

    intruder_count = 0

    def save_face_crop(frame, top, right, bottom, left, count):
        face_crop = frame[top:bottom, left:right]
        folder = "logs/intruders/faces"
        os.makedirs(folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{folder}/intruder_{count}_{timestamp}.jpg"
        cv2.imwrite(filename, face_crop)
        print(f"[!] Intruder face saved: {filename}")
  

    authorized_user = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, faces)

        for (top, right, bottom, left), encoding in zip(faces, encodings):
            matches = face_recognition.compare_faces(known_encodings, encoding)
            name = "Unknown"
            color = (0, 0, 255)  # red

            if True in matches:
                index = matches.index(True)
                name = known_names[index]
                color = (0, 255, 0)  # green
                authorized_user = name
                label = f"✅ {name}"
            else:
                label = f"[!] Intruder #{intruder_count + 1}"
                intruder_count += 1
                log_intruder_snapshot(frame)
                save_face_crop(frame, top, right, bottom, left, intruder_count)

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 20), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, label, (left, top -10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow("Joyce Mode - Face Scan", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if authorized_user:
            speak(f"Welcome, {authorized_user}")
            cap.release()
            cv2.destroyAllWindows()
            return authorized_user

    speak("Intruder Alert! Unknown face detected.")
    cap.release()
    cv2.destroyAllWindows()
    return None

def view_intruder_log():
    log_dir = "logs/intruders"
    if not os.path.exists(log_dir):
        print("[!] Not intruder Snapshot found.")
        return

    files = sorted(os.listdir(log_dir))
    if not files:
        print("[!] Intruder folder is empty.")
        return
    print("\n Intruder Snapshots:\n")
    for file in files:
        print(f"{file}")
        
        last_file = os.path.join(log_dir, files[-1])
        choice = input("\nView last snapshot? y/n: ").lower()
        if choice == "y":
            try:
                subprocess.run(["xdg-open", last_file], check=False)
            except Exception as e:
                print(f"Failed to open image: {e}")
        if choice == "n":
            print("Have a nice day :)")
            return exit
        if choice != "y" and choice != "n":
            print("[!] Unknown command")
            return exit
