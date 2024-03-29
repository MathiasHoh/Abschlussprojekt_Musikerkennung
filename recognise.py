import typing
import os
from multiprocessing import Pool, Lock

import pyaudio
import numpy as np
from tinytag import TinyTag

import constants
from fingerprint import Fingerprint
from storage import SongDatabase


KNOWN_EXTENSIONS = ["mp3", "wav", "flac", "m4a"]


class Recogniser():

    def __init__(self):
        self.__matcher = Matcher()
        self.__database = SongDatabase(
            os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)
                ),
                ".song-db"
            )
        )

    def __get_song_info(self, filename: str) -> typing.Tuple[str, str, str]:
        """Gets the ID3 tags for a file. Returns None for tuple values that don't exist.

        :param filename: Path to the file with tags to read
        :returns: (artist, album, title)
        :rtype: tuple(str/None, str/None, str/None)
        """
        tag = TinyTag.get(filename)
        artist = tag.artist if tag.albumartist is None else tag.albumartist
        return (artist, tag.album, tag.title)
    
    def get_history(self):
        return self.__database.get_history()

    def register_song(
            self,
            filename: str,
            interpret: typing.Optional[str]=None,
            album: typing.Optional[str]=None,
            title: typing.Optional[str]=None
        ):
        """Register a single song.

        Checks if the song is already registered based on path provided and ignores
        those that are already registered.

        :param filename: Path to the file to register"""
        if filename in self.__database:
            return
        
        fingerprint = Fingerprint.from_file(filename)
        _interpret, _album, _title = self.__get_song_info(fingerprint.name)
        song_info = (
            interpret if interpret else _interpret,
            album if album else _album,
            title if title else _title
        )

        try:
            with lock:
                self.__database.store_song(fingerprint.hashes, song_info)

        except NameError:
            # running single-threaded, no lock needed
            self.__database.store_song(fingerprint.hashes, song_info)

    def register_directory(self, path: str):
        """Recursively register songs in a directory.

        :param path: Path of directory to register
        """
        def pool_init(l: Lock):
            """Init function that makes a lock available to each of the workers in
            the pool. Allows synchronisation of db writes since tinydb only supports
            one writer at a time.
            """
            global lock
            lock = l

        to_register = []
        for root, _, files in os.walk(path):
            for f in files:
                if f.split('.')[-1] not in KNOWN_EXTENSIONS:
                    continue

                file_path = os.path.join(path, root, f)
                to_register.append(file_path)

        l = Lock()
        with Pool(constants.NUM_WORKERS, initializer=pool_init, initargs=(l,)) as p:
            p.map(self.register_song, to_register)
    
    def __recognise(self, fingerprint: Fingerprint) -> typing.Union[tuple, str, None]:
        """Recognizes a song based on a fingerprint.

        Args:
            fingerprint (Fingerprint): The fingerprint of the song to be recognized.

        Returns:
            typing.Union[tuple, str, None]: A tuple containing the information about the recognized song (artist, album, title), 
        the song ID if the song was recognized, or None if no match was found.
        """
        matches = self.__database.get_matches(fingerprint.hashes)
        matched_song = self.__matcher.match(matches)
        if matched_song is not None:
            self.__database.add_to_history(matched_song)

        info = self.__database.get_info_for_song_id(matched_song)
        if info is not None:
            return info
        
        return matched_song

    def recognise_song(self, filename: str) -> typing.Union[tuple, str, None]:
        """Recognises a pre-recorded sample.

        Recognises the sample stored at the path ``filename``. The sample can be in any of the
        formats in :data:`recognise.KNOWN_FORMATS`.

        :param filename: Path of file to be recognised.
        :returns: :func:`__get_song_info` result for matched song or None.
        :rtype: tuple(str, str, str)
        """
        fingerprint = Fingerprint.from_file(filename)
        return self.__recognise(fingerprint)

    def listen_to_song(self) -> typing.Union[tuple, str, None]:
        """Recognises a song using the microphone.

        :returns: :func:`__get_song_info` result for matched song or None.
        :rtype: tuple(str, str, str)
        """
        audio = self.__record()
        fingerprint = Fingerprint(audio)
        return self.__recognise(fingerprint)
    
    def __record(self):
        """ Record 5 seconds of audio

        :returns: The audio stream with parameters defined in this module.
        """
        p = pyaudio.PyAudio()

        stream = p.open(format=constants.FORMAT,
                        channels=constants.CHANNELS,
                        rate=constants.RATE,
                        input=True,
                        frames_per_buffer=constants.CHUNK_SIZE)

        frames = []

        for _ in range(0, int(constants.RATE / constants.CHUNK_SIZE * constants.RECORD_SECONDS)):
            data = stream.read(constants.CHUNK_SIZE)
            frames.append(np.frombuffer(data, dtype=np.int16))

        stream.stop_stream()
        stream.close()
        p.terminate()

        return np.hstack(frames)


class Matcher():

    def __init__(self, binwidth: float=0.5):
        """A class providing the scoring capabilities needed for finding the best match of a
        recognised song.

        :parameter binwidth: The bin width in seconds used for the scoring histogram. Defaults to 0.5.
        """
        self.binwidth: float = binwidth

    def __score(self, offsets: list) -> float:
        """Score a matched song.

        Calculates a histogram of the deltas between the time offsets of the hashes from the
        recorded sample and the time offsets of the hashes matched in the database for a song.
        The function then returns the size of the largest bin in this histogram as a score.

        :param offsets: List of offset pairs for matching hashes
        :returns: The highest peak in a histogram of time deltas
        :rtype: int
        """
        tks = list(map(lambda x: x[0] - x[1], offsets))
        hist, _ = np.histogram(
            tks,
            bins=np.arange(
                int(min(tks)),
                int(max(tks)) + self.binwidth + 1,
                self.binwidth
            )
        )
        
        return np.max(hist)

    def match(self, matches: typing.DefaultDict[str, list]) -> typing.Optional[str]:
        """For a dictionary of song_id: offsets, returns the best song_id.

        Scores each song in the matches dictionary and then returns the song_id with the best score.

        :param matches: Dictionary of song_id to list of offset pairs (db_offset, sample_offset)
        as returned by :func:`get_matches`.
        :returns: song_id with the best score.
        :rtype: str
        """
        matched_song = None
        best_score = 0
        for song_id, offsets in matches.items():
            if len(offsets) < best_score:
                # can't be best score, avoid expensive histogram
                continue

            score = self.__score(offsets)
            if score > best_score:
                best_score = score
                matched_song = song_id

        return matched_song
