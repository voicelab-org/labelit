#!/usr/bin/python3
# -*- coding: utf-8 -*-

import librosa
import numpy as np
import os

from labelit.management.scripts.vad import Detector as VaDetector


def add_intermediate_blanks_if_needed(
    inipos, nextstopstart, lcompletestart, lcompleteends, max_len
):
    """Given two time positions, compute intermediate time positions spaced by at most max_len"""

    current_time = inipos
    while nextstopstart > current_time + max_len:
        steppoint = min(current_time + max_len, (current_time + nextstopstart) / 2)
        lcompletestart.append(steppoint)
        lcompleteends.append(steppoint)
        current_time = steppoint


def force_complete_blank(blk_starts, blk_ends, filelength, max_len):
    """Take a list of blanks; return a completed list of blanks with intermediate blanks added if needed to enforce the max_len constraint"""

    final_blk_starts = []
    final_blk_ends = []
    current_time = 0.0

    for start, end in zip(blk_starts, blk_ends):

        add_intermediate_blanks_if_needed(
            current_time, start, final_blk_starts, final_blk_ends, max_len
        )
        final_blk_starts.append(start)
        final_blk_ends.append(end)
        current_time = end
    add_intermediate_blanks_if_needed(
        current_time, filelength, final_blk_starts, final_blk_ends, max_len
    )

    return final_blk_starts, final_blk_ends


def get_cutpoints(
    starts_b, ends_b, record_length, min_seg_length, max_seg_length, keep_all_mode
):
    """Given a list of blanks in audio data, finds out where the audio should be cut to avoid long segments"""

    # Let's first find segments cutpoints (that define segments to analyze; mainly for memory purposes + to avoid to include long blank areas)
    min_voice_length = 0.8
    cutpoints = []
    current_time = 0.0

    for idx, value in enumerate(starts_b):
        current_blank_length = ends_b[idx] - value
        # Blanc d'au moins 0.5 secondes, mérite forcément qu'on coupe, ou alors on a déjà un segment trop long
        if (current_blank_length > 0.5) or (value > (current_time + min_seg_length)):
            # Le signal délimité par ce blanc est d'au moins min_voice_length secondes : il faut l'analyser
            if (value > current_time + min_voice_length) or keep_all_mode:
                cutpoints.append([current_time, value])
            # Dans tous les cas, on avance dans le signal après la coupure
            if keep_all_mode:
                current_time = value
            else:
                current_time = ends_b[idx]

    if keep_all_mode or (record_length > current_time + min_voice_length):
        cutpoints.append([current_time, record_length])
    if len(cutpoints) == 0:
        cutpoints.append([0, record_length])

    return cutpoints


def get_segs(ifile, suppl_args):

    signal, sample_rate = librosa.load(ifile, sr=None)
    filelength = float(len(signal) + 1) / sample_rate

    vad_detector = VaDetector(sample_rate)
    analysis_window_length = vad_detector.window_step
    predictions = vad_detector(signal)

    predictions_diff = predictions[1:] - predictions[:-1]
    segs_ends_blank = [
        analysis_window_length * (x[0] + 2)
        for x in list(np.argwhere(predictions_diff > 0))
    ]
    if predictions[-1] < 1:
        segs_ends_blank.append((len(predictions) + 1) * analysis_window_length)
    if predictions[0] < 1:
        segs_starts_blank = [0.0]
    else:
        segs_starts_blank = []
    segs_starts_blank += [
        analysis_window_length * (x[0] + 1)
        for x in list(np.argwhere(predictions_diff < 0))
    ]

    # To avoid long segments, we need to insert artificial blanks if some are too far away one from another
    segs_starts_blank, segs_ends_blank = force_complete_blank(
        segs_starts_blank, segs_ends_blank, filelength, suppl_args["max_seg_length"]
    )

    # Analyze blank area to return "reasonable" cutpoints
    cutpoints = get_cutpoints(
        segs_starts_blank,
        segs_ends_blank,
        filelength,
        suppl_args["min_seg_length"],
        suppl_args["max_seg_length"],
        suppl_args["continuous_transcript"],
    )

    # Refine cutpoints
    if suppl_args["music_model"] is not None:

        import pickle
        from sklearn import svm

        with open(suppl_args["music_model"], "rb") as hr:
            clf = pickle.load(hr)

        mel_scale = librosa.filters.mel(sr=sample_rate, n_fft=256, n_mels=32)

    selected_cutpoints = []
    for one_cutpoint in cutpoints:
        if suppl_args["continuous_transcript"]:
            # If we want to keep the whole audio, we keep all the sections without condition
            selected_cutpoints.append(one_cutpoint)
            continue
        if one_cutpoint[1] < one_cutpoint[0] + suppl_args["min_seg_length"]:
            continue
        if one_cutpoint[1] > one_cutpoint[0] + suppl_args["max_seg_length"]:
            continue

        if suppl_args["music_model"] is not None:
            start_point = max(0, int(np.round((one_cutpoint[0]) * sample_rate)))
            end_point = min(len(signal), int(np.round((one_cutpoint[1]) * sample_rate)))
            if end_point > start_point + 2 * sample_rate:
                margin = int(((end_point - start_point) - (2 * sample_rate)) // 2)
                to_analyze = signal[
                    start_point + margin : start_point + margin + 2 * sample_rate
                ]
            else:
                to_analyze = np.zeros(2 * sample_rate)
                to_analyze[0 : end_point - start_point] = signal[start_point:end_point]

            spectrogram = librosa.core.stft(
                y=to_analyze, n_fft=256, win_length=160, hop_length=120
            )
            spectrogram_power = np.abs(spectrogram) ** 2
            spectrogram_mel = np.log10(
                np.dot(mel_scale, spectrogram_power) + 1e-6
            ).flatten()

            prediction = clf.predict([spectrogram_mel])[0]

            # Is music seg
            if prediction == 1:
                continue

        selected_cutpoints.append(one_cutpoint)

    return sample_rate, signal, selected_cutpoints


def do_trunk(full_filename, dict_args):
    """Main function: cut the wavefile/writes outputs"""

    sample_rate, signal, cutpoints = get_segs(full_filename, dict_args)
    root = os.path.splitext(full_filename)[0]
    filename = os.path.basename(root)
    basepath = os.path.dirname(root)
    num_segs = len(cutpoints)
    for pos, one_seg in enumerate(cutpoints):
        start_point = max(0, int(np.round((one_seg[0]) * sample_rate)))
        end_point = min(len(signal), int(np.round((one_seg[1]) * sample_rate)))
        bname = (
            "-".join([filename, str(pos), "%.2f" % one_seg[0], "%.2f" % one_seg[1]])
            + ".wav"
        )
        out_fname = os.path.join(basepath, bname)
        librosa.output.write_wav(out_fname, signal[start_point:end_point], sample_rate)
        yield (pos, one_seg[0], one_seg[1], out_fname)


def treat_onefile(entryfile):
    dict_args = {
        "min_seg_length": 1,
        "max_seg_length": 20,
        "music_model": None,
        "continuous_transcript": False,
    }
    existing_keys = set(os.environ.keys())
    if "MIN_SEG_DUR" in existing_keys:
        dict_args["min_seg_length"] = float(os.environ["MIN_SEG_DUR"])
    if "MAX_SEG_DUR" in existing_keys:
        dict_args["max_seg_length"] = float(os.environ["MAX_SEG_DUR"])
    if "MUSIC_MODEL" in existing_keys:
        if os.path.isfile(os.environ["MUSIC_MODEL"]):
            dict_args["music_model"] = os.environ["MUSIC_MODEL"]
    if "CONTINUOUS_TRANSCRIPT" in existing_keys:
        dict_args["continuous_transcript"] = bool(os.environ["CONTINUOUS_TRANSCRIPT"])
    return do_trunk(entryfile, dict_args)
