import os
import subprocess

subprocess.Popen(["python", "bot.py"])

port = os.environ.get("PORT", "5000")

os.execvp(
    "gunicorn",
    ["gunicorn", "--bind", f"0.0.0.0:{port}", "server:app"]
)