# fileUtilities.py
#
# This module provides tools for dealing with
# files on your system.
import pathlib
import json


class JsonFile():
    '''Allows for easy reading/writing of json files.'''
    def __init__(self, path: str):
        self.setPath(path)


    def getPath(self) -> str:
        return self._path
    

    def setPath(self, path: str):
       self._path = path
        

    def read(self) -> dict:
        '''Reads the files, decodes it, and returns a dictionary of the data'''
        with pathlib.Path(generatePath(self.getPath())).open('r', encoding='utf-8') as f:
            return json.loads(''.join([line.strip().replace('\n', '') for line in f]))
    

    def write(self, data: dict):
        with pathlib.Path(generatePath(self.getPath())).open('w', encoding='utf-8') as f:
            json.dump(data, f)


def testFileForIntegrity(file_path: list, folder=False):
    for index, item in enumerate(file_path):
        forbidden_character_list = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        assert type(item) == str, f'expected type <str>, recieved type {type(item)}'
        for character in forbidden_character_list:
            assert character not in item, f'args cannot contain {forbidden_character_list} characters: {item}'
        if not folder:
            if (index == len(file_path) - 1):
                assert '.' in item, f'final location must have an extension: {item}'
            else:
                assert '.' not in item, f'folders may not contain a "." character'


def printDict(dictionary: dict, level: int=0, _recursive=False) -> 'print':
    '''Prints a dictionary in an organized manner.'''
    print(level*'   ' + '{')

    for item in dictionary:
        print(level*'   ', item, end='')
        if type(dictionary[item]) == dict:
            print(':')
            printDict(dictionary[item], (level + 1))
        else:
            print(':\n', (level + 1)*'    ', dictionary[item])

    print(level*'   ' + '}')
        

def generatePath(file_path: str, delimiter='/', folder=False) -> str:
    '''
    Returns a string of a file path. The file path is an extension of the current
    folder this module is working in. Generating paths inside of folders can be done
    by passing thing such as "folder/folder/file.txt".

    The folder parameter can be set to true if the path you are trying to generate is
    a folder.

    The delimiter is what you use to separate folders in the file_path str. The default is /.
    '''
    file_path = list(file_path.split(delimiter))
    testFileForIntegrity(file_path, folder)

    current_folder = pathlib.Path(__file__).parent
    if len(file_path) == 1:
        current_path = current_folder / file_path[0]
    else:
        current_path = current_folder
        for item in file_path:
            current_path = current_path / item

    return str(current_path)


def fileExists(file_path: str, delimiter='/') -> bool:
    '''
    Returns a bool whether the specified file exists or not
    '''
    if pathlib.Path(generatePath(file_path, delimiter)).exists():
        return True
    return False


def getFileSizeMB(file_path: str, delimiter='/') -> float:
    if fileExists(file_path):
        return round(pathlib.Path(generatePath(file_path, delimiter)).stat().st_size / 1024 / 1024, 2)
    raise OSError(f'file not found at: {file_path}')


def getFileName(file_path: str, delimiter='/', extension=False):
    '''Returns the name of the file (and extension if configured)'''
    if fileExists(file_path):
        file = pathlib.Path(generatePath(file_path, delimiter))
        return file.stem if not extension else file.name
    raise OSError(f'file not found at: {file_path}')