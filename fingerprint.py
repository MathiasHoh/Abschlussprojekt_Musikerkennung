import uuid
import constants
import numpy as np
import numpy.typing as np_types
from pydub import AudioSegment
from scipy.signal import spectrogram
from scipy.ndimage import maximum_filter


class Fingerprint():

    @classmethod
    def from_file(cls, file_path: str) -> "Fingerprint":
        """Generate hashes for a file.

        Given a file, runs it through the fingerprint process to produce a list of hashes from it.

        :param filename: The path to the file.
        :returns: A :class:`Fingerprint` instance.
        """
        a = AudioSegment.from_file(file_path).set_channels(1).set_frame_rate(constants.SAMPLE_RATE)
        frames = np.frombuffer(a.raw_data, np.int16)
        return cls(frames, file_path)

    def __init__(self, audio: np_types.ArrayLike, name: str="recorded"):
        self.name: str = name
        self.hashes: list = self.__fingerprint_audio(audio, name)
    
    def __fingerprint_audio(self, frames: np_types.ArrayLike, name: str) -> list:
        """Generate hashes for a series of audio frames.

        Used when recording audio.

        :param frames: A mono audio stream. Data type is any that ``scipy.signal.spectrogram`` accepts.
        :returns: The output of :func:`hash_points`.
        """
        nperseg = int(constants.SAMPLE_RATE * constants.FFT_WINDOW_SIZE)
        f, t, Sxx =  spectrogram(frames, constants.SAMPLE_RATE, nperseg=nperseg)
        peaks = self.__idxs_to_tf_pairs(self.__find_peaks(Sxx), t, f)
        return self.__hash_points(peaks, name)

    def __find_peaks(self, Sxx: np_types.NDArray) -> np_types.NDArray:
        """Finds peaks in a spectrogram.

        Uses :data:`~abracadabra.constants.PEAK_BOX_SIZE` as the size of the region around each
        peak. Calculates number of peaks to return based on how many peaks could theoretically
        fit in the spectrogram and the :data:`~abracadabra.constants.POINT_EFFICIENCY`.

        Inspired by
        `photutils
        <https://photutils.readthedocs.io/en/stable/_modules/photutils/detection/core.html#find_peaks>`_.

        :param Sxx: The spectrogram.
        :returns: A list of peaks in the spectrogram.
        """
        data_max = maximum_filter(Sxx, size=constants.PEAK_BOX_SIZE, mode='constant', cval=0.0)
        peak_goodmask = (Sxx == data_max)  # good pixels are True
        y_peaks, x_peaks = peak_goodmask.nonzero()
        peak_values = Sxx[y_peaks, x_peaks]
        i = peak_values.argsort()[::-1]
        # get co-ordinates into arr
        j = [(y_peaks[idx], x_peaks[idx]) for idx in i]
        total = Sxx.shape[0] * Sxx.shape[1]
        # in a square with a perfectly spaced grid, we could fit area / PEAK_BOX_SIZE^2 points
        # use point efficiency to reduce this, since it won't be perfectly spaced
        # accuracy vs speed tradeoff
        peak_target = int((total / (constants.PEAK_BOX_SIZE**2)) * constants.POINT_EFFICIENCY)
        return j[:peak_target]

    def __idxs_to_tf_pairs(self, idxs: np_types.NDArray, t: np_types.NDArray, f: np_types.NDArray) -> np_types.NDArray:
        """Helper function to convert time/frequency indices into values."""
        return np.array([(f[i[0]], t[i[1]]) for i in idxs])
    
    def __hash_points(self, points: np_types.NDArray, filename: str) -> list:
        """Generates all hashes for a list of peaks.

        Iterates through the peaks, generating a hash for each peak within that peak's target zone.

        :param points: The list of peaks.
        :param filename: The filename of the song, used for generating song_id.
        :returns: A list of tuples of the form (hash, time offset, song_id).
        """
        hashes = []
        song_id = uuid.uuid5(uuid.NAMESPACE_OID, filename).int
        for anchor in points:
            for target in self.__target_zone(
                anchor, points, constants.TARGET_T, constants.TARGET_F, constants.TARGET_START
            ):
                hashes.append((
                    # hash
                    self.__hash_point_pair(anchor, target),
                    # time offset
                    anchor[1],
                    # filename
                    str(song_id)
                ))
        return hashes

    def __hash_point_pair(self, p1: np_types.NDArray, p2: np_types.NDArray) -> int:
        """Helper function to generate a hash from two time/frequency points."""
        return hash((p1[0], p2[0], p2[1]-p2[1]))

    def __target_zone(self, anchor: np_types.NDArray, points: np_types.NDArray, width: float, height: int, t: float) -> np_types.NDArray:
        """Generates a target zone as described in `the Shazam paper
        <https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf>`_.

        Given an anchor point, yields all points within a box that starts `t` seconds after the point,
        and has width `width` and height `height`.

        :param anchor: The anchor point
        :param points: The list of points to search
        :param width: The width of the target zone
        :param height: The height of the target zone
        :param t: How many seconds after the anchor point the target zone should start
        :returns: Yields all points within the target zone.
        """
        x_min = anchor[1] + t
        x_max = x_min + width
        y_min = anchor[0] - (height*0.5)
        y_max = y_min + height
        for point in points:
            if point[0] < y_min or point[0] > y_max:
                continue
            if point[1] < x_min or point[1] > x_max:
                continue
            yield point


if __name__ == "__main__":
    # Beispiel
    audio_file_name = "Test.mp3"
    fp = Fingerprint.from_file(audio_file_name)
    fp.hashes
    fp.name
