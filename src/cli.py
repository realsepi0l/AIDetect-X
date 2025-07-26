import typer
import cv2
from src import phishing_detector, facial_auth
from src.joyce_mode import joyce_mode
from utils.face_utils import recognize_face_live, view_intruder_log 

app = typer.Typer()

@app.command()
def scan_email(file: str, auth: bool = False):
    """
    Scan an email text file for phishing indicators.
    Optionally require face verification first.
    """
    if auth:
        typer.echo("🔒 Facial verification required...")
        if not facial_auth.recognize_live():
            typer.secho("❌ Access denied: Face not recognized.", fg=typer.colors.RED)
            raise typer.Exit()

    is_phishing, confidence = phishing_detector.scan_email(file)
    if is_phishing:
        typer.secho(f"⚠ Phishing Detected! ({confidence * 100:.2f}% confidence)", fg=typer.colors.RED, bold=True)
    else:
        typer.secho(f"✅ This email is safe. ({confidence * 100:.2f}% confidence)", fg=typer.colors.GREEN)

@app.command()
def joyce():
    """Run real-time face recognition + phishing detection."""
    joyce_mode()

@app.command()
def intruder_log():
    """ Locate Intruder Logs + Snapshots """
    view_intruder_log()

if __name__ == "__main__":
    app()

