# videoDownload.py
#
# This module provides tools for downloading
# videos off of the internet.

# standard libraries
import urllib.request
import random

# 3rd party
# pip install -U yt-dlp
import yt_dlp

# local modules
import fileUtilities
import pathlib


class VideoConnectionError(Exception):
    """Raised when cannot connect."""


def generateRandomNumber(low: int, high: int) -> int:
    return random.randint(low, high)


def generateRandomMP4(
    folder_path: str, name: str, extension: str, delimiter: str = "/"
) -> str:
    """
    Generates a random path to a .mp4 file at the given
    folder_path (relative to current module position).
    """
    folder_path = list(folder_path.split(delimiter))
    folder_path.append(name)
    # If file with the same name is found,
    # creates a new unique name so as to not override the original.
    while pathlib.Path(delimiter.join(folder_path) + extension).exists():
        folder_path[-1] = str(generateRandomNumber(0, 999999999))
    path = delimiter.join(folder_path)
    folder_path[-1] += extension
    fileUtilities.testFileForIntegrity(folder_path)
    return path + extension


def video_download(
    url: str, folder_path: str, name: str, extension: str, delimiter: str = "/"
) -> str:
    """
    Downloads a video given a link and outputs the video to the folder_path.
    Returns the file name.
    Download supports:
        - Youtube
        - Twitter
    """
    path = generateRandomMP4(folder_path, name, extension, delimiter)
    try:
        urllib.request.urlopen(url)
    except Exception:
        raise VideoConnectionError

    # Download
    try:
        ydl_opts = {"outtmpl": path}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError:
        raise VideoConnectionError

    return path.split(delimiter)[-1]


if __name__ == "__main__":
    print(">>> Running in DEV MODE...")
    user_input = input("Enter a URL:")

    try:
        video_return = video_download(user_input, "src/vid")
        print(f">>> CONNECTED")
        print(f">>> CREATED src/vid/{video_return} SUCCESSFULLY")

    except Exception as e:
        if type(e) == VideoConnectionError:
            print(">>> COULD NOT CONNECT")
        else:
            raise e
