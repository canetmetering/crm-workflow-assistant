import subprocess
import time
from browser_launcher import launch_chrome_with_debugging


def run(command):
    subprocess.run(
        command,
        shell=True,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def kill_old_sessions():
    print("Killing old sessions...", flush=True)
    commands = [
        "pkill -9 chrome",
        "pkill -9 chromium",
        "pkill -9 chromium-browser",
        "pkill -9 Xvfb",
        "pkill -9 x11vnc",
        "pkill -9 fluxbox",
        "pkill -9 websockify",
    ]
    for command in commands:
        run(command)
    time.sleep(3)


def start_remote_desktop():
    print("Starting remote desktop...", flush=True)

    subprocess.Popen(
        "Xvfb :99 -screen 0 1920x1080x24",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(4)

    subprocess.Popen(
        "DISPLAY=:99 fluxbox",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(4)

    subprocess.Popen(
        "x11vnc -display :99 -forever -shared -nopw -listen 0.0.0.0 -rfbport 5900",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(4)

    subprocess.Popen(
        "websockify --web=/usr/share/novnc/ 6080 localhost:5900",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(4)


def boot_ascent_environment():
    kill_old_sessions()
    start_remote_desktop()
    launch_chrome_with_debugging()
    print("Boot sequence complete.", flush=True)


if __name__ == "__main__":
    boot_ascent_environment()
