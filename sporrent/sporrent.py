import threading
import os
import subprocess
import time
import signal
from dotenv import load_dotenv

load_dotenv()
TORRENTS = os.getenv("TORRENTS")
READY = os.getenv("READY")
DOWNLOADING = os.getenv("DOWNLOADING")
CLIENT = os.getenv("CLIENT")
DWS = os.getenv("DWS")
CONFIG  = os.getenv("CONFIG")

def start_download(name: str):
    # Set up term handler
    try:
        # Remove progress from last torrents; just to be sure (bugs appear)
        # Progress is saved in ~/.config/transmission/x/filename.torrent;
        # where x is "resume" and "torrents". So, look inside both of them.
        for dir in ["resume", "torrents"]:
            # Walk thru the files in the directory
            try:
                _, _, files = next(os.walk(os.path.join(CONFIG, dir)))
            except StopIteration:
                print("No progress found in {}".format(dir))
                continue

            for f in files:
                # Look for the name in the file. The progress file has some random
                # characters (i.e. file.asojdf839.resume) appended to the end of it's name, so
                # we look for the sub-string containing our torrent name.
                if name.strip(".torrent") in f:
                    try:
                        path = os.path.join(CONFIG, dir, f)
                        os.remove(path)
                    except OSError:
                        pass
            

        print("Starting to download {}"
                .format(DOWNLOADING + name))
        # We launch transmission-cli to download the DOWNLOADING + name torrent in the READY folder
        proc = subprocess.Popen((CLIENT, "-w", READY, DOWNLOADING + name),
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        # We read the transmission-cli output until we see the Complete substring.
        # Randomly, though, it would jump into Seeding without warning, so we look for that as well.
        while True:
            line = proc.stdout.readline()
            print(line.decode("utf-8"))
            if "Complete" in str(line) or "Seeding" in str(line):
                break

        # Print the success, kill the process and remove the torrent
        print("Downloaded {}".format(name))
        proc.kill()
        os.remove(os.path.join(DOWNLOADING, name))

    except OSError as e:
        print(e)
        return


def main():
    print("Starting process")

    # Set up term handler
    # term = Term()

    # For the first round
    first = True
    try:
        # while not term.term:
        while True:
            # If first round, look for files in .downloading
            if first:
                dir = DOWNLOADING
            else:
                dir = TORRENTS
            # Walk thru files in the selected dir
            _, _, files = next(os.walk(dir))
            for f in files:
                if f.endswith(".torrent"):
                    # If it was first round, we don't have to move anything
                    if not first:
                        # Move the torrents to the .downloading folder
                        os.rename(TORRENTS + f, DOWNLOADING + f)
                    
                    # Launch a thread to start download the file
                    print("Launching: {}".format(f))
                    th = threading.Thread(target=start_download,
                                     args=(f,),
                                     daemon=True)
                    th.start()
            
            # If it was first round, low the flag
            if first:
                first = False
            
            # Else, sleep for a fixed amount of time
            else:
                time.sleep(5 * 60)

    except OSError as e:
        print(e)
        return

"""
class Term:
    term = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.end)
        signal.signal(signal.SIGTERM, self.end)

    def end(self):
        self.term = True
"""

if __name__ == "__main__":
    main()
