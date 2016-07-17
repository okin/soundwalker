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


def fail_if_no_message(iterator):
    message_retrieved = False
    for message in iterator:
        message_retrieved = True
        yield message

    if not message_retrieved:
        pytest.fail("No message returned.")


@pytest.mark.parametrize("filename", [
    pytest.mark.xfail('05-Cool_Artist-Song_B.ogg'),
    pytest.mark.xfail('05-cool_artist-song_b.mp3'),
    'foo.pdb',
    'foo.mp3.orig',
    '01 - titel.mp3',
    pytest.mark.xfail('02-Beewax-Bring_the_Queen_(Feat._Bee_Power).mp3'),
])
def test_good_filename(filename):
    for message in fail_if_no_message(soundwalker.check_filename(filename)):
        print(message)
        assert message


@pytest.mark.parametrize("name", [
    ' Bla',
    'Bla ',
    ' Bla ',
    pytest.mark.xfail('Correctly Named (2015)'),
    pytest.mark.xfail('Twin - Double Disc (2CD) (1989)'),
])
def test_album_name(name):
    for message in fail_if_no_message(soundwalker.check_album_name(name)):
        print(message)
        assert message


@pytest.mark.parametrize("name", [
    ' CD 3 ',
    'something',
    'foo 123',
    'disc 1',
    'CD 1 -',
    pytest.mark.xfail('CD 578'),
    pytest.mark.xfail("CD 75 - Additional Description"),
])
def test_disc_folder_naming(name):
    for message in fail_if_no_message(soundwalker.check_disc_name(name)):
        print(message)
        assert message


@pytest.mark.parametrize("filenames", [
    ('01-a.mp3', '01-A.mp3'),
    ['01-b.mp3', '01-a.mp3'],
])
def test_finding_duplicates(filenames):
    for message in fail_if_no_message(soundwalker.exist_duplicate_files(filenames)):
        print(message)
        assert message
