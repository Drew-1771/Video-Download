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


class FileNameError(Exception):
    """Raised when filename cannot be determined after download."""


def generateRandomNumber(low: int, high: int) -> int:
    return random.randint(low, high)


def video_download(url: str, path: str, isPlaylist=False) -> (str, int):
    """
    Downloads a video given a link and outputs the video to the folder_path.
    Returns the file size.
    -1 means download was successful but error w/ size calculation
    """

    # probe for connection
    try:
        urllib.request.urlopen(url)
    except Exception:
        # if twitter url, replace x.com w/ twitter.com
        if "x.com" in url:
            url = url.replace("x.com", "twitter.com")
            print("trying x.com -> twitter.com")
            return video_download(url, path, isPlaylist=isPlaylist)
        raise VideoConnectionError

    # Download
    file_path = None
    try:
        ydl_opts = {
            "outtmpl": f"{path}.%(ext)s",
            "playlist_items": "1",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            try:
                file_path = pathlib.Path(path).parent / (
                    pathlib.Path(path).name + "." + info_dict["ext"]
                )
            except KeyError:
                try:
                    file_path = pathlib.Path(path).parent / (
                        pathlib.Path(path).name + "." + info_dict["entries"][0]["ext"]
                    )
                except KeyError:
                    # file size could not be calculated for some reason
                    raise FileNameError
    except yt_dlp.utils.DownloadError:
        raise VideoConnectionError

    return file_path


if __name__ == "__main__":
    print(">>> Running in DEV MODE...")
    user_input = input("Enter a URL:")

    where = "src/vid/" + str(generateRandomNumber(0, 9999999))

    try:
        video_return = video_download(user_input, where)
        print(f">>> CONNECTED")
        print(f">>> CREATED {video_return} SUCCESSFULLY")

    except Exception as e:
        if type(e) == VideoConnectionError:
            print(">>> COULD NOT CONNECT")
        else:
            raise e
