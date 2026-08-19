from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import BatchNormalization, Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
TOKENS_PATH = MODEL_DIR / "training_tokens.json"
MODEL_PATH = MODEL_DIR / "lumatonemodel.keras"
VOCAB_PATH = MODEL_DIR / "music_vocab.json"
SEEDS_PATH = MODEL_DIR / "seed_patterns.json"

SEQUENCE_LENGTH = 64


def main():
    tokens = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
    vocabulary = sorted(set(tokens))
    token_to_int = {token: i for i, token in enumerate(vocabulary)}
    int_to_token = {str(i): token for token, i in token_to_int.items()}

    sequences = []
    targets = []

    for i in range(len(tokens) - SEQUENCE_LENGTH):
        sequences.append([token_to_int[t] for t in tokens[i:i + SEQUENCE_LENGTH]])
        targets.append(token_to_int[tokens[i + SEQUENCE_LENGTH]])

    x = np.array(sequences, dtype="float32").reshape((-1, SEQUENCE_LENGTH, 1))
    x /= float(len(vocabulary))
    y = to_categorical(targets, num_classes=len(vocabulary))

    model = Sequential([
        LSTM(192, input_shape=(SEQUENCE_LENGTH, 1), return_sequences=True),
        Dropout(0.25),
        LSTM(192, return_sequences=True),
        BatchNormalization(),
        Dropout(0.2),
        LSTM(96),
        Dense(128, activation="relu"),
        Dropout(0.2),
        Dense(len(vocabulary), activation="softmax"),
    ])

    model.compile(loss="categorical_crossentropy", optimizer="adam")

    callbacks = [
        EarlyStopping(monitor="loss", patience=5, restore_best_weights=True),
        ModelCheckpoint(str(MODEL_PATH), monitor="loss", save_best_only=True),
    ]

    model.fit(
        x,
        y,
        epochs=40,
        batch_size=64,
        callbacks=callbacks,
        verbose=1,
    )

    VOCAB_PATH.write_text(
        json.dumps({
            "sequence_length": SEQUENCE_LENGTH,
            "token_to_int": token_to_int,
            "int_to_token": int_to_token,
        }, indent=2),
        encoding="utf-8",
    )

    seed_count = min(40, len(sequences))
    seed_indices = np.linspace(0, len(sequences) - 1, seed_count, dtype=int)
    seeds = [sequences[i] for i in seed_indices]
    SEEDS_PATH.write_text(json.dumps(seeds), encoding="utf-8")

    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
