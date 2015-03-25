#! /usr/bin/env python

import os
import re

SOUND_FILE_EXTENSIONS = set(['.mp3', '.cue', '.flac', '.ogg', '.m3u'])
COVER_FILE_EXTENSIONS = set(['.jpg', '.jpeg'])

_VALID_FILE_EXTENSIONS = tuple(SOUND_FILE_EXTENSIONS.union(COVER_FILE_EXTENSIONS))
_FILENAME_REGEX = re.compile('^(?P<tracknumber>\d+)-(?P<artist>[a-zA-Z0-9_]+)-(?P<title>[a-zA-Z0-9_]+)\.(?P<fileextension>[a-zA-Z0-9]+)$')


def walk(path, *, is_artist=False, is_album=False):
    process_artist = False
    process_albums = False
    for (dirpath, directories, filenames) in os.walk(path):
        for filename in filenames:
            # TODO: handle files inside multi-disc-album
            is_good_file(filename)

        for directory in directories:
            if is_artist:
                is_good_album_name(directory)
                process_albums = True
            elif is_album:
                is_good_disc_name(directory)
            else:
                process_artist = True

            walk(os.path.join(dirpath, directory),
                 is_artist=process_artist,
                 is_album=process_albums)


def is_good_file(name):
    if not name.endswith(_VALID_FILE_EXTENSIONS):
        print("Additional file: {}".format(name))
        return False

    filenameMatch = _FILENAME_REGEX.match(name)
    if filenameMatch is None:
        print("Filename does not match the expected pattern: "
              "02-Artist_A-Title_T.mp3")
        return False

    return True


def is_good_album_name(name):
    if not name_must_not_be_stripped(name):
        return False

    if '(' not in name and ')' not in name:
        print("Folder '{}' misses attributes - i.e. year.".format(name))
        return False

    return True


def name_must_not_be_stripped(name):
    if not name == name.strip():
        if name.endswith(' ') and name.endswith(' '):
            print("Folder '{}' has spaces at front and end.".format(name))
        elif name.startswith(' '):
            print("Folder '{}' has spaces at front.".format(name))
        elif name.endswith(' '):
            print("Folder '{}' has spaces at end.".format(name))

        return False

    return True


def is_good_disc_name(name):
    if not name_must_not_be_stripped(name):
        return False

    if not name.startswith('CD'):
        print("Folder '{}' does not start with 'CD'.".format(name))
        return False

    folderNameMatch = re.search('^CD (?P<disc>\d+)( - (?P<additional>.+)){0,1}$',
                                name)

    if not folderNameMatch:
        print("Folder '{}' does not follow disc pattern: "
              "CD 7 - Additional Description")

        try:
            int(name[-1:])
        except ValueError:
            print("Folder '{}' does not end with a number.".format(name))

        return False

    return True

if __name__ == '__main__':
    # TODO: read argv
    walk()
