import shutil
import subprocess

def send_notification(title: str, message: str, icon: str = "package-x-generic", urgency: str = "normal"):
    """
    Sends desktop notification via notify-send.
    """
    if shutil.which("notify-send"):
        try:
            subprocess.run([
                "notify-send",
                "-a", "Allzip",
                "-i", icon,
                "-u", urgency,
                title,
                message
            ], check=False)
        except Exception:
            pass
