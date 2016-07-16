#! /usr/bin/env python
# -*- coding: utf-8 -*-

import soundwalker

import pytest


@pytest.mark.parametrize("filename", [ 
    '05-Cool_Artist-Song_B.ogg',
    '05-cool_artist-song_b.mp3',
    pytest.mark.xfail('foo.pdb'),
    pytest.mark.xfail('foo.mp3.orig'),
    pytest.mark.xfail('01 - titel.mp3'),
])
def test_good_filename(filename):
    assert soundwalker.is_good_file(filename)


@pytest.mark.parametrize("name", [
    pytest.mark.xfail(' Bla'),
    pytest.mark.xfail('Bla '),
    pytest.mark.xfail(' Bla '),
    'Correctly Named (2015)',
    'Double (2CD) (1989)',
])
def test_album_name(name):
    assert soundwalker.is_good_album_name(name)


@pytest.mark.parametrize("name", [
    pytest.mark.xfail(' CD 3 '),
    pytest.mark.xfail('something'),
    pytest.mark.xfail('foo 123'),
    pytest.mark.xfail('disc 1'),
    pytest.mark.xfail('CD 1 -'),
    'CD 578',
    "CD 75 - Additional Description",
])
def test_disc_folder_nanimg(name):
    assert soundwalker.is_good_disc_name(name)


@pytest.mark.parametrize("filenames", [
    ('01-a.mp3', '01-A.mp3'),
    ['01-b.mp3', '01-a.mp3'],
])
def test_finding_duplicates(filenames):
    assert soundwalker.exist_duplicate_files(filenames)
