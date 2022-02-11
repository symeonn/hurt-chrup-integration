import ftplib
import os
import sys

from constants import HURT_HOSTNAME, HURT_USERNAME, HURT_PASSWORD, LOCAL_FILE_PATH


def fetch_file_from_hurt_ftp(filename):
    ftp_server = ftplib.FTP(HURT_HOSTNAME, HURT_USERNAME, HURT_PASSWORD)
    # ftp_server.dir()
    ftp_server.encoding = 'CP850'

    print(filename)
    print(os.path.join(sys.path[0], LOCAL_FILE_PATH, filename))
    with open(os.path.join(sys.path[0], LOCAL_FILE_PATH, filename), "wb") as file:
        ftp_server.retrbinary(f"RETR {filename}", file.write)

    ftp_server.quit()
