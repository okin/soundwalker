# Copyright (C) 2016  Niko Wenselowski
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import soundwalker

import pytest


@pytest.mark.parametrize("filename", [ 
    '05-Cool_Artist-Song_B.ogg',
    '05-cool_artist-song_b.mp3',
    pytest.mark.xfail('foo.pdb'),
    pytest.mark.xfail('foo.mp3.orig'),
    pytest.mark.xfail('01 - titel.mp3'),
    '02-Anthrax-Bring_The_Noise_(Feat._Public_Enemy).mp3',
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
