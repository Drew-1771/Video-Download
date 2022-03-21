# videoDownload.py
#
# This module provides tools for downloading
# videos off of the internet.

# standard libraries
from typing import NamedTuple
import urllib.request
import urllib.parse
import random

# 3rd party
# pip install -U yt-dlp
import yt_dlp

# local modules
import fileUtilities
import twitter_video_dl


class ReturnTuple(NamedTuple):
        url: str
        file_name: str
        file_size: str
        connection: bool
        done: bool


class VideoConnectionError(Exception):
    '''Raised when cannot connect.'''

class InputError(Exception):
    '''Raised when there is an input error in dev mode'''


def generateRandomNumber(low: int, high: int) -> int:
    return random.randint(low, high)


def generateRandomMP4(folder_path: str, delimiter='/') -> str:
    '''
    Generates a random path to a .mp4 file at the given 
    folder_path (relative to current module position).
    '''
    folder_path, name = list(folder_path.split(delimiter)), str(generateRandomNumber(0, 999999999)) + '.mp4'
    folder_path.append(name)
    # If file with the same name is found, 
    # creates a new unique name so as to not override the original.
    while fileUtilities.fileExists(delimiter.join(folder_path)):
        folder_path.pop()
        name = str(generateRandomNumber(0, 999999999)) + '.mp4'
        folder_path.append(name)
    path = delimiter.join(folder_path)
    fileUtilities.testFileForIntegrity(folder_path)
    return path


def youtube_download(url: str, folder_path: str, delimiter='/') -> str:
    '''
    Downloads a youtube video given a link and outputs the video to the folder_path. 
    Returns the file name.
    '''
    path = generateRandomMP4(folder_path, delimiter)
    try:
        urllib.request.urlopen(url)
    except Exception:
        raise VideoConnectionError

    # Download
    ydl_opts = {'outtmpl': path}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    return path.split(delimiter)[-1]


def twitter_download(url: str, folder_path: str, delimiter='/') -> str:
    '''
    Downloads a twitter video given a link and outputs the video to the folder_path. 
    Returns the file name.
    '''
    path = generateRandomMP4(folder_path, delimiter)
    try:
        urllib.request.urlopen(url)
    except Exception:
        raise VideoConnectionError

    # Download
    try:
        twitter_video_dl.download_video(url, path)
    except AssertionError:
        raise VideoConnectionError
    return path.split(delimiter)[-1]


if __name__ == '__main__':
    print('>>> Running in DEV MODE...')
    mode = input("Which download?: Y (Youtube, default), T (Twitter): ").lower()
    user_input = input('Enter a URL:')

    try:
        if (mode in ("", "y")):
            video_return = youtube_download(user_input, "src/vid")
        elif (mode == "t"):
            video_return = twitter_download(user_input, "src/vid")
        else:
            raise InputError
        print(f'>>> CONNECTED')
        print(f'>>> CREATED vid/{video_return} SUCCESSFULLY')

    except Exception as e:
        if type(e) == VideoConnectionError:
            print('>>> COULD NOT CONNECT')
        else:
            raise e