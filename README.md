# LumaTone – Music Generation Application

LumaTone is a simple and interactive music generation application that creates original instrumental music based on different musical styles and user-selected settings.

The application allows users to choose a music style, adjust the length and energy of the generated piece, listen to the result directly in the browser, and download the generated MIDI file.

## 🎵 Live Demo

**Streamlit App:** https://lumatone-music.streamlit.app/

## Features

- **Generate original instrumental music**
- **Choose from multiple musical styles**
- **Adjust the length of the generated music**
- **Control the energy level**
- **Listen to generated music directly in the application**
- **Download generated music as MIDI files**
- **Generate different musical variations using the same settings**

## Music Styles

LumaTone currently provides four different styles:

- **Six-String Sprint** – Quick and energetic guitar-inspired riffs
- **Royal Raga** – Indian classical-inspired melodic phrases with a steady drone
- **Sunroom Piano** – Warm and calm piano-led melodies
- **Midnight Pulse** – Upbeat electronic rhythms and synth-inspired melodies

## Technologies Used

- **Python** – Core programming language
- **Streamlit** – Interactive web application interface
- **MIDI** – Music representation and file generation
- **Music generation algorithms** – Used to create note patterns, melodies, rhythms, and variations

## Project Structure

```text
LumaTone_MusicGenerator/
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   └── midi/
│
├── generated/
│
├── models/
│
├── composer.py
├── learn_model.py
├── prepare_midi.py
├── streamlit_app.py
│
├── requirements.txt
├── requirements-training.txt
├── README.md
└── .gitignore
```

## How It Works

**1.** Select a musical style
**2.** Adjust the desired music length and energy
**3.** Generate a new piece
**4.** Listen to the generated result in the browser
**5.** Download the generated MIDI file.

Each generation can produce a different musical variation, allowing users to experiment with different combinations of styles and settings.

## Project Goal

The goal of LumaTone is to demonstrate how musical note patterns and MIDI sequences can be combined with a simple interactive interface to create an accessible music-generation application.

The project focuses on making music creation simple and approachable while allowing users to experiment with different musical styles and generation settings.

## Future Improvements

Possible future improvements include:

- **Adding more musical styles**
- **Adding more instruments**
- **Improving melody and rhythm variation**
- **Adding additional audio formats**
- **Providing more control over musical parameters**
- **Improving the user interface and playback experience**

## Author

**Shanzay Kamran**

Developed as part of a music-generation application project.
