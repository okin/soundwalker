#! /usr/bin/env python3

import argparse
import os
import re
import sys
from itertools import chain

UNWANTED_CHARACTERS = "',&äöüÄÖÜ"
SOUND_FILE_EXTENSIONS = set(['.mp3', '.cue', '.flac', '.ogg', '.m3u'])
COVER_FILE_EXTENSIONS = ('.jpg', '.jpeg')
SPECIAL_ENTRIES_TO_IGNORE = set(('@eaDir', '.DS_Store'))

_VALID_FILE_EXTENSIONS = tuple(SOUND_FILE_EXTENSIONS.union(set(COVER_FILE_EXTENSIONS)))
_FILENAME_REGEX = re.compile('^(?P<tracknumber>\d+)-(?P<artist>[a-zA-Z0-9_]+)-(?P<title>[a-zA-Z0-9_().-]+)\.(?P<fileextension>[a-zA-Z0-9]+)$')


def runAsScript():
    parser = argparse.ArgumentParser()
    parser.add_argument('--artist-dir', dest="artist", action="store_true")
    parser.add_argument('--album-dir', dest="album", action="store_true")
    parser.add_argument('directory', nargs='?', default='.')
    args = parser.parse_args()

    for message in walk(args.directory, is_artist=args.artist, is_album=args.album):
        print(message)


def walk(path, *, is_artist=False, is_album=False, include_fullpath=True):
    process_artist = False
    process_albums = False

    for entry in os.scandir(path):
        if entry.name in SPECIAL_ENTRIES_TO_IGNORE:
            continue

        if entry.is_file():
            if entry.name.endswith(COVER_FILE_EXTENSIONS):
                continue
            messages = is_good_file(entry.name)
        elif entry.is_dir():
            messages = []
            if is_album:
                filenames = set(f.name for f in os.scandir(entry.path) if f.is_file())

                messages = exist_duplicate_files(filenames)
                continue

            for directory in (d for d in os.scandir(entry.path) if d.is_dir()):
                if is_artist:
                    messages = chain(messages, check_album_name(directory.name))
                    process_albums = True
                elif is_album:
                    messages = chain(messages, check_disc_name(directory.name))
                else:
                    process_artist = True

                dirMessages = ("{}/{}".format(directory.name, message)
                               for message in walk(directory.path,
                                                   is_artist=process_artist,
                                                   is_album=process_albums,
                                                   include_fullpath=False))

                messages = chain(messages, dirMessages)

        for message in messages:
            if include_fullpath:
                yield "{}/{}".format(entry.path, message)
            else:
                yield "{}: {}".format(entry.name, message)



def is_good_file(name):
    if not name.endswith(_VALID_FILE_EXTENSIONS):
        yield "Additional file"

    filenameMatch = _FILENAME_REGEX.match(name)
    if filenameMatch is None:
        for char in UNWANTED_CHARACTERS:
            if char in name:
                yield "Unwanted character: {0!r}".format(char)
                break
        else:
            yield ("Filename does not match the expected pattern: "
                   "02-Artist_A-Title_T.mp3".format(name))


def exist_duplicate_files(filenames):
    # if not len(filenames) == len(set(name.lower() for name in filenames)):
    #     return  # Fast check succeeded

    duplicate_numbers = set()
    track_numbers = {}
    for name in filenames:
        try:
            match = _FILENAME_REGEX.match(name)
            number = int(match.group('tracknumber'))
        except AttributeError:
            try:
                number = int(name.split('-')[0])
            except (ValueError, IndexError):
                yield "Unable to get track# for {0}".format(name)
                continue

        if number in track_numbers:
            yield ("Duplicate track number {num!r} on files "
                   "{0!r} and {1}".format(track_numbers[number],
                                          name, num=number))
            duplicate_numbers.add(number)
        else:
            track_numbers[number] = name

    # TODO: duplicate check!
    # return bool(duplicate_numbers)


def check_album_name(name):
    yield from name_space_check(name)

    if '(' not in name or ')' not in name:
        yield "Folder misses attributes - i.e. year.".format(name)


def name_space_check(name):
    if not name == name.strip():
        if name.endswith(' ') and name.endswith(' '):
            yield "Folder has spaces at front and end.".format(name)
        elif name.startswith(' '):
            yield "Folder has spaces at front.".format(name)
        elif name.endswith(' '):
            yield "Folder has spaces at end.".format(name)


def check_disc_name(name):
    yield from name_space_check(name)

    if not name.startswith('CD'):
        yield "Folder {!r} does not start with 'CD'.".format(name)
        return

    folderNameMatch = re.search('^CD (?P<disc>\d+)( - (?P<additional>.+)){0,1}$',
                                name)

    if not folderNameMatch:
        yield ("Folder {!r} does not follow disc pattern: "
               "CD 7 - Additional Description")

        try:
            int(name[-1:])
        except ValueError:
            yield "Folder {!r} does not end with a number.".format(name)

if __name__ == '__main__':
    runAsScript()
