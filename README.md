# AIDetect-X

# AIDetect-X

AIDetect-X is a command-line cybersecurity utility that detects phishing emails and analyzes facial data using machine learning. Built with Python, PyTorch, and Scikit-learn, this tool is crafted for red team ops and AI-based threat detection.

Features

"scan-email" — Scan an email text file for phishing indicators using ML classifiers.
"face-check" — Run facial recognition on an input image and report match/confidence.

Installation

git clone https://github.com/your-username/AIDetect-X.git
cd AIDetect-X
pip install -r requirements.txt

Usage
python main.py scan-email /path/to/your/email.txt
python main.py face-check /path/to/your/face.png
