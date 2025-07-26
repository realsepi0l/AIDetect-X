def load_face_encodings(known_dir):
    encodings = []
    names = []
    for file in os.listdir(known_dir):
        path = os.path.join(known_dir, file)
        if os.path.isdir(path):
            continue  # Skip directories
        if file.endswith(('.pkl', '.jpg', '.jpeg', '.png')):
            with open(path, 'rb') as f:
                try:
                    encoding = pickle.load(f)
                    encodings.append(encoding)
                    names.append(os.path.splitext(file)[0])
                except Exception as e:
                    print(f"❌ Failed to load encoding from {file}: {e}")
    return encodings, names

