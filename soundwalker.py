#! /usr/bin/env python

import os
import re

SOUND_FILE_EXTENSIONS = set(['.mp3', '.cue', '.flac', '.ogg', '.m3u'])
COVER_FILE_EXTENSIONS = set(['.jpg', '.jpeg'])


def walk(path, directories, filenames, is_artist=False, is_album=False):
    if is_artist:
        for filename in filenames:
            if not filename.endswith(SOUND_FILE_EXTENSIONS):
                print("Additional file: {}".format(os.path.join(path, filename)))


    for (dirpath, directories, filenames) in os.walk(path):
        pass


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
