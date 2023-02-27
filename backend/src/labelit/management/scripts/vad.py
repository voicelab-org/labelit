import numpy as np


def geometric_mean(data):
    """Geometric mean"""

    return np.exp(np.log(data).mean(axis=1))


def safe_flatness(data):
    """Negative log-flatness with special care for rows that comport 0s"""

    output = np.zeros(data.shape[0])
    entirely_not_null_rows = data.all(axis=1)

    # No problem for rows without 0s; rows with 0s should be infinite, capped here to max values to be consistent with environment
    output[entirely_not_null_rows] = -10 * np.log10(
        geometric_mean(data[entirely_not_null_rows, :])
        / np.mean(data[entirely_not_null_rows, :], axis=1)
    )
    output[np.invert(entirely_not_null_rows)] = max(output)

    return output


class Detector:
    """Main class that performs the VAD detection"""

    def __init__(self, signal_sampling_rate=None, window_step=None, stereo_mode=True):
        """Initialization, mainly setup all config. variables/thresholds"""

        self.signal_sampling_rate = (
            signal_sampling_rate if signal_sampling_rate is not None else 8000
        )
        self.window_step = window_step if window_step is not None else 0.025

        self.base_pitch_threshold = 185
        self.base_spectral_flatness_threshold = 5
        self.base_energy_threshold = (
            10  # Multiplier between squared noise power best estimate and "speech"
        )

        self.post_filter_apply = True  # Wether we want to "smooth"/"refine" initial predictions; cheap version of a Viterbi decoding
        self.post_filter_min_silence = 0.25
        self.post_filter_min_speech = 0.125
        self.post_filter_min_silence_run_points = int(
            np.round(self.post_filter_min_silence / self.window_step)
        )
        self.post_filter_min_speech_run_points = int(
            np.round(self.post_filter_min_speech / self.window_step)
        )

        # We work on windows of size...
        self.window_step_points = int(
            np.round(self.window_step * self.signal_sampling_rate)
        )
        self.window_size_points = int(
            np.round(2 * self.window_step * self.signal_sampling_rate)
        )

        # Compute coherent FFTs...
        self.fft_points = pow(2, int(np.ceil(np.log2(self.window_size_points))))
        self.fft_kept_coeffs = int(np.ceil((self.fft_points - 1) / 2))
        self.fft_bins_freq_increment = self.signal_sampling_rate / self.fft_points

        # How to find initial thresholds
        self.prefilter_energy_threshold = (
            30  # Multiplier between squared noise power first estimate and "speech"
        )
        if stereo_mode:
            self.ini_energy_thresh_percentile = 20
        else:
            self.ini_energy_thresh_percentile = 8
        self.ini_pitch_thresh_percentile = 25
        self.ini_flatness_thresh_percentile = 1

        # Memory related parameters
        self.max_points = 10000000
        self.max_windows = int(np.ceil(self.max_points / self.window_size_points))

    def __call__(self, audio_data):
        """Apply VAD on data"""

        # First pad data before extracting chunks
        self.num_windows = int(np.ceil((len(audio_data) - 1) / self.window_step_points))
        self.padded_data = np.zeros(
            self.window_size_points + self.num_windows * self.window_step_points
        )
        self.padded_data[0 : len(audio_data)] = audio_data

        # First pass analysis on audio + prediction analysis (no speech at first)
        self.extract_stats()
        self.predictions = np.zeros(self.num_windows)

        # We need to study more cautiously only frames with a minimum level of energy
        for window_index in np.where(np.invert(self.low_energy_prefilter))[0]:
            # Speech prediction can be triggered by pitch, flatness and energy
            speech_detected = (
                (
                    self.logpowers[window_index]
                    >= np.log(self.base_energy_threshold * self.thresh_min_power)
                )
                or (
                    self.flatness[window_index]
                    >= (
                        self.thresh_min_flatness + self.base_spectral_flatness_threshold
                    )
                )
                or (
                    self.pitches[window_index]
                    >= (self.thresh_min_pitch + self.base_pitch_threshold)
                )
            )

            if speech_detected:
                # Store prediction
                self.predictions[window_index] = 1
            else:
                # Update barycentric estimation of silence energy levels
                self.thresh_min_power = (
                    self.thresh_min_power * self.silence_count
                    + self.powers[window_index]
                ) / (self.silence_count + 1)
                self.silence_count += 1

        # Potential refinment
        if self.post_filter_apply:
            self.post_filter()

        # Return as int for compatibility issues (useful to get "regions" by diff)
        return self.predictions.astype(int)

    def extract_stats(self):
        """First coarse analysis pass to get stats on signal"""

        # Do not keep entire FFTs/chunked frames in memory
        self.pitches = np.zeros(self.num_windows, dtype=float)
        self.powers = np.zeros(self.num_windows, dtype=float)
        self.flatness = np.zeros(self.num_windows, dtype=float)

        # Rather compute huge matrices only for portions of audio
        for window_start in range(0, self.num_windows, self.max_windows):
            # Extact frames for portion
            window_end = min(self.num_windows, window_start + self.max_windows)
            frames = np.array(
                [
                    self.padded_data[
                        win_num
                        * self.window_step_points : win_num
                        * self.window_step_points
                        + self.window_size_points
                    ]
                    for win_num in range(window_start, window_end)
                ]
            )
            fft_data = abs(
                np.fft.fft(frames, self.fft_points)[:, 1 : self.fft_kept_coeffs]
            )

            # Compute descriptors for current signal portion
            self.pitches[
                window_start:window_end
            ] = self.fft_bins_freq_increment * np.argmax(fft_data, axis=1)
            self.powers[window_start:window_end] = np.sum(pow(fft_data, 2), axis=1)
            self.flatness[window_start:window_end] = safe_flatness(fft_data)

        # Specific case: region with *very* low energy are seen as silence without other checks, allow to init silence energy levels
        self.logpowers = np.log(self.powers + 1e-12)
        self.low_energy_prefilter = self.logpowers < np.percentile(
            self.logpowers, self.ini_energy_thresh_percentile
        ) + np.log(self.prefilter_energy_threshold)
        self.silence_count = np.sum(self.low_energy_prefilter)
        self.thresh_min_power = np.exp(self.logpowers[self.low_energy_prefilter].mean())

        # Other values are initialized according to their distribution
        self.thresh_min_pitch = np.percentile(
            self.pitches, self.ini_pitch_thresh_percentile
        )
        self.thresh_min_flatness = np.percentile(
            self.flatness, self.ini_flatness_thresh_percentile
        )

    def ignore_symbol_if_shorter_than(self, symbol, min_len):
        """Useful for post-filtering: given a symbol, suppress occurences of that symbol if not repeated at least min_len times"""

        last_area_begin = -1
        is_in_area = False

        # Let's go sequentially through data
        for index in range(self.num_windows):
            # Start a region if i. symbol spotted ii. not already inside a region & keep track of beginning index
            if self.predictions[index] == symbol:
                if not is_in_area:
                    is_in_area = True
                    last_area_begin = index
            # Close a region if i. was inside a region ii. not the symbol anymore
            else:
                if is_in_area:
                    is_in_area = False
                    # If the region was too short, delete occurrences of the symbol in that region
                    if index < last_area_begin + min_len:
                        self.predictions[last_area_begin:index] = not (symbol)

        # Special case: a region may not have been closed at the end of data
        if is_in_area:
            if self.num_windows < last_area_begin + min_len:
                self.predictions[last_area_begin:] = not (symbol)

    def post_filter(self):
        """Improves prediction by post-filtering"""

        # Filter silences, then filter speech regions
        self.ignore_symbol_if_shorter_than(
            False, self.post_filter_min_silence_run_points
        )
        self.ignore_symbol_if_shorter_than(True, self.post_filter_min_speech_run_points)
