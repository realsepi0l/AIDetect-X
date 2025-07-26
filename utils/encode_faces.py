# utils/encode_faces.py

import os
import face_recognition
import pickle

def encode_known_faces(input_dir='data/faces/known', output_file='models/face_encodings.pkl'):
    encodings = []
    names = []

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(input_dir, filename)
            image = face_recognition.load_image_file(path)
            boxes = face_recognition.face_locations(image)

            if boxes:
                enc = face_recognition.face_encodings(image, boxes)[0]
                encodings.append(enc)
                names.append(os.path.splitext(filename)[0])
                print(f"✅ Encoded {filename}")
            else:
                print(f"⚠ No face found in {filename}")

    with open(output_file, 'wb') as f:
        pickle.dump((encodings, names), f)
    print(f"[✅] Encodings saved to {output_file}")

if __name__ == '__main__':
    encode_known_faces()

