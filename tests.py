#! /usr/bin/env python
# -*- coding: utf-8 -*-

import soundwalker


def test_file_name():
    assert not soundwalker.is_good_file('foo.pdb')

    assert soundwalker.is_good_file('foo.mp3')
    assert soundwalker.is_good_file('foo.ogg')

    assert not soundwalker.is_good_file('foo.mp3.orig')


def test_album_name():
    assert not soundwalker.is_good_album_name(' Bla')
    assert not soundwalker.is_good_album_name('Bla ')
    assert not soundwalker.is_good_album_name(' Bla ')

    assert soundwalker.is_good_album_name('Correctly Named (2015)')

    assert soundwalker.is_good_album_name('Double (2CD) (1989)')


def test_disc_folder_nanimg():
    assert not soundwalker.is_good_disc_name(' CD 3 ')
    assert not soundwalker.is_good_disc_name('something')
    assert not soundwalker.is_good_disc_name('foo 123')
    assert not soundwalker.is_good_disc_name('disc 1')
    assert soundwalker.is_good_disc_name('CD 578')

    assert not soundwalker.is_good_disc_name('CD 1 -')
    assert soundwalker.is_good_disc_name("CD 75 - Additional Description")
