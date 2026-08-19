from __future__ import annotations

import json
from pathlib import Path

from music21 import chord, converter, note

BASE_DIR = Path(__file__).resolve().parent
MIDI_DIR = BASE_DIR / "data" / "midi"
MODEL_DIR = BASE_DIR / "models"
TOKENS_PATH = MODEL_DIR / "training_tokens.json"

MODEL_DIR.mkdir(exist_ok=True)


def event_token(element) -> str | None:
    if isinstance(element, note.Note):
        pitch_part = str(int(element.pitch.midi))
    elif isinstance(element, chord.Chord):
        pitch_part = ".".join(str(int(p.midi)) for p in element.pitches)
    else:
        return None

    duration = round(float(element.duration.quarterLength), 2)
    return f"{pitch_part}|{duration}"


def extract_tokens() -> list[str]:
    tokens: list[str] = []

    midi_files = sorted(list(MIDI_DIR.glob("*.mid")) + list(MIDI_DIR.glob("*.midi")))
    if not midi_files:
        raise SystemExit("Add MIDI files to data/midi/ before running this script.")

    for midi_file in midi_files:
        score = converter.parse(str(midi_file))
        for element in score.recurse().notes:
            token = event_token(element)
            if token:
                tokens.append(token)

    if len(tokens) < 200:
        raise SystemExit("Not enough note data. Add more MIDI files and try again.")

    TOKENS_PATH.write_text(json.dumps(tokens, indent=2), encoding="utf-8")
    print(f"Saved {len(tokens)} training events to {TOKENS_PATH}")


if __name__ == "__main__":
    extract_tokens()
