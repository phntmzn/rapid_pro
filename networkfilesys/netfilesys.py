import subprocess
import requests
from requests.auth import HTTPBasicAuth
from ftplib import FTP

# --- AFP (Apple Filing Protocol) ---
def mount_afp(url, mount_point):
    subprocess.run(['mount_afp', url, mount_point], check=True)

# Example usage:
# mount_afp("afp://user:pass@192.168.1.10/Share", "/Volumes/Nexus")


# --- NFS (Network File System) ---
def mount_nfs(remote_path, mount_point):
    subprocess.run(['sudo', 'mount_nfs', '-o', 'resvport', remote_path, mount_point], check=True)

# Example usage:
# mount_nfs("192.168.1.10:/exports/share", "/Volumes/nfs_mount")


# --- SMB (Preferred Modern Network FS) ---
def mount_smb(user, password, host, share, mount_point):
    url = f"//{user}:{password}@{host}/{share}"
    subprocess.run(['mount_smbfs', url, mount_point], check=True)

# Example usage:
# mount_smb("user", "pass", "192.168.1.20", "Share", "/Volumes/smb_mount")


# --- FTP Access (Read-Only, Not Mounted) ---
def list_ftp_files(host, user, password, path):
    ftp = FTP(host)
    ftp.login(user, password)
    ftp.cwd(path)
    files = ftp.nlst()
    ftp.quit()
    return files

# Example usage:
# print(list_ftp_files("ftp.example.com", "user", "pass", "/path"))


# --- WebDAV (via HTTP request and mount) ---
def download_webdav_file(url, user, password):
    response = requests.get(url, auth=HTTPBasicAuth(user, password))
    print(response.text)

# Example usage:
# download_webdav_file("https://host/webdav/file.txt", "user", "pass")


def mount_webdav(url, mount_point):
    subprocess.run(['mount_webdav', '-s', url, mount_point], check=True)

# Example usage:
# mount_webdav("https://user:pass@host/webdav", "/Volumes/webdav_mount")
