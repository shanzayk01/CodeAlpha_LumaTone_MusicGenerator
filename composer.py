from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from music21 import chord, instrument, note, stream

BASE_DIR = Path(__file__).resolve().parent
GENERATED_DIR = BASE_DIR / "generated"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "lumatonemodel.keras"
VOCAB_PATH = MODEL_DIR / "music_vocab.json"
SEEDS_PATH = MODEL_DIR / "seed_patterns.json"

GENERATED_DIR.mkdir(exist_ok=True)

MAJOR = [0, 2, 4, 5, 7, 9, 11]
MINOR = [0, 2, 3, 5, 7, 8, 10]

STYLE_BOOK = {
    "six-string sprint": {
        "label": "Six-String Sprint",
        "scale": MINOR,
        "keys": [(52, "E minor"), (57, "A minor")],
        "tempo_range": (152, 172),
        "progression": [0, 5, 2, 6],
        "programs": {"lead": 30, "rhythm": 29, "low": 33},
        "titles": ["Open Road", "Fast Lane", "Afterburn", "Redline", "Side Street"],
    },
    "royal raga": {
        "label": "Royal Raga",
        "scale": MINOR,
        "keys": [(60, "C"), (62, "D")],
        "tempo_range": (90, 102),
        "progression": [0],
        "programs": {"lead": 104, "rhythm": 104, "low": 32},
        "titles": ["Evening Courtyard", "Quiet Mehfil", "Amber Sky", "Moonlit Hall", "Still Garden"],
    },
    "sunroom piano": {
        "label": "Sunroom Piano",
        "scale": MAJOR,
        "keys": [(60, "C major"), (65, "F major"), (67, "G major")],
        "tempo_range": (86, 104),
        "progression": [0, 4, 5, 3],
        "programs": {"lead": 0, "rhythm": 0, "low": 0},
        "titles": ["Window Light", "Slow Sunday", "First Coffee", "Open Curtains", "Warm Floorboards"],
    },
    "midnight pulse": {
        "label": "Midnight Pulse",
        "scale": MINOR,
        "keys": [(57, "A minor"), (60, "C minor"), (62, "D minor")],
        "tempo_range": (126, 142),
        "progression": [0, 5, 3, 6],
        "programs": {"lead": 81, "rhythm": 89, "low": 38},
        "titles": ["Night Drive", "City Signal", "Blue Neon", "Late Train", "Streetlights"],
    },
}


def _pitch(tonic: int, scale: List[int], degree: int, octave_shift: int = 0) -> int:
    octave, index = divmod(int(degree), 7)
    return tonic + scale[index] + 12 * octave + 12 * octave_shift


def _add(events: List[dict], pitches, start, duration, role, velocity):
    if not isinstance(pitches, list):
        pitches = [pitches]
    pitches = sorted({max(28, min(96, int(p))) for p in pitches})
    events.append({
        "pitches": pitches,
        "start": round(float(start), 3),
        "duration": round(float(duration), 3),
        "role": role,
        "velocity": max(30, min(120, int(velocity))),
    })


def _load_model_bundle():
    if not (MODEL_PATH.exists() and VOCAB_PATH.exists() and SEEDS_PATH.exists()):
        return None
    try:
        from tensorflow.keras.models import load_model

        model = load_model(MODEL_PATH)
        vocab = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
        seeds = json.loads(SEEDS_PATH.read_text(encoding="utf-8"))
        return model, vocab, seeds
    except Exception:
        return None


def _token_to_event(token: str) -> Tuple[List[int], float]:
    pitch_part, duration_part = token.rsplit("|", 1)
    duration = float(duration_part)
    if "." in pitch_part:
        pitches = [int(p) for p in pitch_part.split(".")]
    else:
        pitches = [int(pitch_part)]
    return pitches, duration


def _model_notes(length: int, energy: float):
    bundle = _load_model_bundle()
    if bundle is None:
        return None

    model, vocab, seeds = bundle
    int_to_token = {int(k): v for k, v in vocab["int_to_token"].items()}
    pattern = list(random.choice(seeds))
    seq_len = int(vocab["sequence_length"])
    n_vocab = len(vocab["token_to_int"])
    temperature = max(0.35, min(1.45, energy))

    output = []
    for _ in range(length):
        x = np.array(pattern, dtype="float32").reshape(1, seq_len, 1)
        x /= float(n_vocab)
        prediction = np.asarray(model.predict(x, verbose=0)[0], dtype=np.float64)
        prediction = np.log(np.maximum(prediction, 1e-9)) / temperature
        probability = np.exp(prediction - prediction.max())
        probability /= probability.sum()
        index = int(np.random.choice(len(probability), p=probability))
        output.append(_token_to_event(int_to_token[index]))
        pattern = pattern[1:] + [index]

    return output


def _six_string(tonic, scale, bars, energy):
    events = []
    progression = STYLE_BOOK["six-string sprint"]["progression"]
    leads = [
        [7, 9, 10, 11, 10, 9, 7, 9],
        [11, 13, 14, 13, 11, 10, 9, 7],
        [14, 13, 11, 10, 11, 13, 14, 16],
        [9, 10, 11, 13, 11, 10, 9, 7],
    ]

    for bar in range(bars):
        start = bar * 4.0
        root_degree = progression[bar % len(progression)]
        root = _pitch(tonic, scale, root_degree)
        fifth = root + 7
        octave = root + 12

        # Tight power-chord pattern
        for step in range(8):
            if step in {0, 2, 4, 6} or random.random() < 0.55:
                _add(events, [root, fifth, octave], start + step * 0.5, 0.28, "rhythm",
                     92 if step in {0, 4} else 78)

        for step in range(8):
            low = root - 12 if step not in {3, 7} else fifth - 12
            _add(events, low, start + step * 0.5, 0.34, "low", 74 if step in {0, 4} else 64)

        phrase = leads[bar % len(leads)].copy()
        if energy > 1.0 and random.random() < 0.3:
            phrase = random.choice(leads).copy()

        for i, degree in enumerate(phrase):
            duration = 0.24 if i % 2 else 0.31
            if bar == bars - 1 and i == len(phrase) - 1:
                degree = 7
                duration = 0.9
            _add(events, _pitch(tonic, scale, degree), start + i * 0.5, duration, "lead",
                 93 if i in {0, 4} else 82 + random.randint(-4, 4))

        if bar % 4 == 2:
            fill = [14, 16, 17, 18, 17, 16, 14, 13]
            for i, degree in enumerate(fill):
                _add(events, _pitch(tonic, scale, degree), start + 2 + i * 0.25, 0.18, "lead", 88)

    return events


def _royal_raga(tonic, scale, bars, energy):
    events = []
    phrases = [
        [7, 8, 9, 8, 7, 6, 7, 8],
        [7, 8, 9, 10, 11, 10, 9, 8],
        [11, 13, 11, 10, 11, 9, 10, 8],
        [14, 12, 13, 11, 10, 11, 9, 8],
        [8, 9, 10, 11, 13, 11, 10, 9],
        [6, 7, 8, 9, 8, 7, 6, 7],
    ]
    rhythms = [
        [0.5] * 8,
        [0.75, 0.25, 0.5, 0.5, 0.75, 0.25, 0.5, 0.5],
        [0.5, 0.5, 0.75, 0.25, 0.5, 0.5, 0.5, 0.5],
    ]

    for bar in range(bars):
        start = bar * 4.0
        # Sa-Pa-Sa bed
        _add(events, [tonic - 12, tonic - 5, tonic], start, 3.92, "rhythm", 46)
        # Soft low pulses
        for pos, p in [(0.0, tonic - 24), (1.5, tonic - 17), (2.0, tonic - 24), (3.5, tonic - 17)]:
            _add(events, p, start + pos, 0.36, "low", 54)

        phrase = phrases[bar % len(phrases)].copy()
        if energy > 1.0 and random.random() < 0.25:
            phrase = random.choice(phrases).copy()
        if bar == bars - 1:
            phrase = [11, 9, 10, 8, 7, 8, 7, 7]

        rhythm = random.choice(rhythms)
        cursor = 0.0
        for i, (degree, duration) in enumerate(zip(phrase, rhythm)):
            if energy > 1.1 and i not in {0, len(phrase)-1} and random.random() < 0.12:
                degree += random.choice([-1, 1])
            pitch = _pitch(tonic, scale, max(5, min(15, degree)))
            _add(events, pitch, start + cursor, max(0.22, duration * 0.9), "lead",
                 82 + (5 if degree % 7 in {2, 5} else 0) + random.randint(-3, 3))
            cursor += duration

    return events


def _sunroom_piano(tonic, scale, bars, energy):
    events = []
    progression = STYLE_BOOK["sunroom piano"]["progression"]
    contours = [
        [7, 9, 11, 10, 9, 8, 7, 9],
        [9, 10, 11, 13, 11, 10, 9, 8],
        [7, 8, 9, 11, 10, 9, 8, 7],
    ]

    for bar in range(bars):
        start = bar * 4.0
        root_degree = progression[bar % len(progression)]
        chord_degrees = [root_degree, root_degree + 2, root_degree + 4]
        chord_pitches = [_pitch(tonic, scale, d, -1) for d in chord_degrees]

        # Broken chord
        pattern = [0, 1, 2, 1, 0, 1, 2, 1]
        for i, idx in enumerate(pattern):
            _add(events, chord_pitches[idx], start + i * 0.5, 0.44, "rhythm", 58 if i not in {0,4} else 64)

        _add(events, _pitch(tonic, scale, root_degree, -2), start, 1.85, "low", 62)
        _add(events, _pitch(tonic, scale, root_degree + 4, -2), start + 2, 1.75, "low", 56)

        contour = contours[bar % len(contours)]
        for i, degree in enumerate(contour):
            if energy > 1.05 and random.random() < 0.14:
                degree += random.choice([-1, 1])
            if bar == bars - 1 and i == len(contour) - 1:
                degree = 7
            _add(events, _pitch(tonic, scale, degree), start + i * 0.5, 0.4, "lead",
                 76 + random.randint(-4, 4))

    return events


def _midnight_pulse(tonic, scale, bars, energy):
    events = []
    progression = STYLE_BOOK["midnight pulse"]["progression"]
    motifs = [
        [7, 9, 10, 12, 10, 9, 7, 9],
        [9, 10, 12, 14, 12, 10, 9, 7],
        [14, 12, 10, 9, 10, 12, 14, 16],
    ]

    for bar in range(bars):
        start = bar * 4.0
        root_degree = progression[bar % len(progression)]
        chord_pitches = [_pitch(tonic, scale, d, -1) for d in [root_degree, root_degree + 2, root_degree + 4]]

        # Off-beat synth chops
        for step in range(8):
            pos = start + step * 0.5
            if step % 2 == 1 or random.random() < 0.4:
                _add(events, chord_pitches, pos, 0.30, "rhythm", 64 if step % 2 else 55)

        root = _pitch(tonic, scale, root_degree, -2)
        fifth = _pitch(tonic, scale, root_degree + 4, -2)
        for step in range(8):
            _add(events, root if step not in {3,7} else fifth, start + step * 0.5, 0.36, "low",
                 70 if step in {0,4} else 60)

        motif = motifs[bar % len(motifs)]
        for i, degree in enumerate(motif):
            if energy > 1.05 and random.random() < 0.16:
                degree += random.choice([-1, 1])
            if bar == bars - 1 and i == len(motif) - 1:
                degree = 7
            _add(events, _pitch(tonic, scale, degree), start + i * 0.5, 0.27, "lead",
                 84 + random.randint(-4, 5))

    return events


def _blend_model(events: List[dict], model_notes, tonic, scale, energy):
    if not model_notes:
        return

    leads = [e for e in events if e["role"] == "lead"]
    if not leads:
        return

    allowed = [_pitch(tonic, scale, d) for d in range(5, 22)]
    chance = min(0.28, max(0.08, energy * 0.12))

    i = 0
    for event in leads:
        if random.random() > chance:
            continue
        source, _ = model_notes[i % len(model_notes)]
        i += 1
        if not source:
            continue
        p = int(source[0])
        while p < 58:
            p += 12
        while p > 90:
            p -= 12
        event["pitches"] = [min(allowed, key=lambda x: abs(x - p))]


def _midi_program(style_key: str, role: str) -> int:
    return STYLE_BOOK[style_key]["programs"][role]


def _write_midi(events: List[dict], style_key: str, filename: str):
    score = stream.Score()

    for role in ("rhythm", "low", "lead"):
        part = stream.Part()
        part.id = role.title()

        inst = instrument.Instrument()
        inst.midiProgram = _midi_program(style_key, role)
        part.insert(0, inst)

        for event in events:
            if event["role"] != role:
                continue
            if len(event["pitches"]) == 1:
                element = note.Note(event["pitches"][0])
            else:
                element = chord.Chord(event["pitches"])
            element.duration.quarterLength = float(event["duration"])
            element.volume.velocity = int(event["velocity"])
            part.insert(float(event["start"]), element)

        score.insert(0, part)

    path = GENERATED_DIR / filename
    score.write("midi", fp=str(path))
    return path


def compose(style_key: str, length: int = 96, energy: float = 0.85):
    if style_key not in STYLE_BOOK:
        style_key = "sunroom piano"

    cfg = STYLE_BOOK[style_key]
    tonic, key_name = random.choice(cfg["keys"])
    tempo = random.randint(*cfg["tempo_range"])
    scale = cfg["scale"]
    bars = max(8, min(24, int(round(length / 6))))
    energy = max(0.35, min(1.45, float(energy)))

    if style_key == "six-string sprint":
        events = _six_string(tonic, scale, bars, energy)
    elif style_key == "royal raga":
        events = _royal_raga(tonic, scale, bars, energy)
    elif style_key == "midnight pulse":
        events = _midnight_pulse(tonic, scale, bars, energy)
    else:
        events = _sunroom_piano(tonic, scale, bars, energy)

    model_notes = _model_notes(max(24, bars * 3), energy)
    if style_key != "royal raga":
        _blend_model(events, model_notes, tonic, scale, energy)

    events.sort(key=lambda e: (e["start"], e["role"]))

    title = random.choice(cfg["titles"])
    filename = f"{style_key.replace(' ', '-')}-{random.randint(100000, 999999)}.mid"
    _write_midi(events, style_key, filename)

    return {
        "title": title,
        "filename": filename,
        "events": events,
        "tempo": tempo,
        "bars": bars,
        "style": style_key,
        "style_label": cfg["label"],
        "key": key_name,
        "source": "pattern model" if model_notes else "music engine",
    }
