import os
import argparse

# --- List disk and tty devices ---
def list_dev_devices():
    print("Devices in /dev:")
    for entry in os.listdir("/dev"):
        if entry.startswith("disk") or entry.startswith("tty"):
            print(f"  {entry}")

# --- FIFO pipe path ---
pipe_path = "/tmp/mypipe"

if not os.path.exists(pipe_path):
    os.mkfifo(pipe_path)

# --- Write to named pipe ---
def writer():
    with open(pipe_path, 'w') as fifo:
        fifo.write("Hello from FIFO\n")

# --- Read from named pipe ---
def reader():
    with open(pipe_path, 'r') as fifo:
        print("Received:", fifo.read())

# --- CLI Usage Instructions ---
def show_reference():
    print("""
# Pseudo File System Commands:
ls -l /dev        # devfs: devices
ls -l /dev/fd     # fdesc: file descriptors
lsof -p $$        # show your current open fds
df -h             # may show virtual mounts
mount             # shows mounted pseudo filesystems
""")

# --- Main entry ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pseudo FS tool")
    parser.add_argument("--write", action="store_true", help="Write to FIFO")
    parser.add_argument("--read", action="store_true", help="Read from FIFO")
    parser.add_argument("--show-devices", action="store_true", help="List disk/tty devices in /dev")
    parser.add_argument("--reference", action="store_true", help="Show pseudo FS reference commands")

    args = parser.parse_args()

    if args.show_devices:
        list_dev_devices()
    if args.write:
        writer()
    if args.read:
        reader()
    if args.reference:
        show_reference()

"""
python3 pseudo_fs.py --show-devices
python3 pseudo_fs.py --write
python3 pseudo_fs.py --read
python3 pseudo_fs.py --reference
"""
