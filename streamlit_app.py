from __future__ import annotations

import json

import streamlit as st
import streamlit.components.v1 as components

from composer import GENERATED_DIR, STYLE_BOOK, compose

st.set_page_config(
    page_title="LumaTone",
    page_icon="♫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

STYLE_ORDER = [
    "six-string sprint",
    "royal raga",
    "sunroom piano",
    "midnight pulse",
]

st.markdown(
    """
    <style>
    :root {
        --paper: #f7f5f0;
        --card: #ffffff;
        --ink: #1f2933;
        --muted: #6b7280;
        --line: #dedbd3;
        --soft: #ece8df;
        --accent: #285c7a;
        --accent-soft: #e8f0f4;
    }

    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif !important;
    }

    .stApp {
        background: var(--paper);
        color: var(--ink);
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        max-width: 1120px;
        padding-top: 2.4rem;
        padding-bottom: 3rem;
    }

    .topline {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 18px;
        border-bottom: 1px solid var(--line);
        margin-bottom: 32px;
    }

    .brand {
        font-size: 22px;
        font-weight: 750;
        letter-spacing: -0.6px;
    }

    .brand-note {
        font-size: 12px;
        color: var(--muted);
    }

    .intro {
        max-width: 720px;
        margin-bottom: 28px;
    }

    .intro h1 {
        margin: 0 0 10px;
        font-size: 42px;
        line-height: 1.08;
        letter-spacing: -1.4px;
        font-weight: 760;
        color: var(--ink);
    }

    .intro p {
        margin: 0;
        max-width: 640px;
        color: var(--muted);
        font-size: 15px;
        line-height: 1.65;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--card);
        border: 1px solid var(--line) !important;
        border-radius: 14px;
        box-shadow: none;
    }

    label, .stSelectbox label, .stSlider label {
        color: #374151 !important;
        font-size: 12px !important;
        font-weight: 650 !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 9px !important;
        border-color: #d7d4cc !important;
        background: #fff !important;
    }

    .stButton > button {
        min-height: 46px;
        border-radius: 9px;
        border: 1px solid var(--accent);
        background: var(--accent);
        color: #fff;
        box-shadow: none;
        font-weight: 700;
    }

    .stButton > button:hover {
        background: #214d66;
        border-color: #214d66;
        color: #fff;
    }

    [data-testid="stDownloadButton"] button {
        min-height: 44px;
        border-radius: 9px;
        border: 1px solid #cfd3d6;
        background: #ffffff;
        color: var(--ink);
        box-shadow: none;
        font-weight: 650;
    }

    .side-note {
        padding: 2px 2px 8px;
        color: var(--muted);
        font-size: 12px;
        line-height: 1.6;
    }

    .track-card {
        padding: 2px 2px 8px;
    }

    .track-top {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 18px;
        margin-bottom: 16px;
    }

    .track-title {
        color: var(--ink);
        font-size: 25px;
        font-weight: 760;
        letter-spacing: -0.5px;
    }

    .track-style {
        margin-top: 5px;
        color: var(--muted);
        font-size: 12px;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        border: 1px solid #d8e2e7;
        border-radius: 999px;
        padding: 6px 10px;
        background: var(--accent-soft);
        color: var(--accent);
        font-size: 11px;
        font-weight: 700;
        white-space: nowrap;
    }

    .track-meta {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin-bottom: 14px;
    }

    .meta-box {
        border-top: 1px solid var(--line);
        padding-top: 10px;
    }

    .meta-box b {
        display: block;
        color: var(--ink);
        font-size: 15px;
        margin-bottom: 2px;
    }

    .meta-box span {
        color: var(--muted);
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: .05em;
    }

    .empty {
        min-height: 360px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 28px;
    }

    .empty strong {
        display: block;
        margin-bottom: 7px;
        font-size: 18px;
    }

    .empty span {
        display: block;
        max-width: 390px;
        color: var(--muted);
        font-size: 13px;
        line-height: 1.65;
    }

    .footer-line {
        margin-top: 28px;
        padding-top: 16px;
        border-top: 1px solid var(--line);
        color: #8b8f93;
        font-size: 11px;
    }

    @media (max-width: 800px) {
        .block-container {
            padding: 1.4rem 1rem 2.5rem;
        }

        .intro h1 {
            font-size: 34px;
        }

        .topline {
            margin-bottom: 24px;
        }

        .track-meta {
            grid-template-columns: 1fr 1fr 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="topline">
        <div class="brand">LumaTone</div>
        <div class="brand-note">Music sketchbook</div>
    </div>
    <div class="intro">
        <h1>Make a fresh instrumental idea.</h1>
        <p>Pick a mood, set the length and energy, then create a new track. Listen in the browser or keep the MIDI file.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([0.34, 0.66], gap="large")

with left:
    with st.container(border=True):
        style = st.selectbox(
            "Sound",
            STYLE_ORDER,
            format_func=lambda key: STYLE_BOOK[key]["label"],
            index=0,
        )

        length = st.slider(
            "Track length",
            min_value=48,
            max_value=168,
            value=96,
            step=12,
        )

        energy = st.slider(
            "Energy",
            min_value=0.35,
            max_value=1.45,
            value=0.85,
            step=0.05,
        )

        generate = st.button("Create track", use_container_width=True)

        st.markdown(
            """
            <div class="side-note">
                Every click creates a new variation. The same settings can still produce a different melody and arrangement.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if generate:
        with st.spinner("Writing a new track..."):
            st.session_state["track"] = compose(
                style_key=style,
                length=length,
                energy=energy,
            )

track = st.session_state.get("track")

with right:
    with st.container(border=True):
        if not track:
            st.markdown(
                """
                <div class="empty">
                    <div>
                        <strong>Nothing playing yet</strong>
                        <span>Choose a sound on the left and create a track. The player and download button will appear here.</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="track-card">
                    <div class="track-top">
                        <div>
                            <div class="track-title">{track["title"]}</div>
                            <div class="track-style">{track["style_label"]}</div>
                        </div>
                        <div class="pill">{track["source"].title()}</div>
                    </div>

                    <div class="track-meta">
                        <div class="meta-box"><b>{track["tempo"]}</b><span>BPM</span></div>
                        <div class="meta-box"><b>{track["key"]}</b><span>Key</span></div>
                        <div class="meta-box"><b>{track["bars"]}</b><span>Bars</span></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            events_json = json.dumps(track["events"])
            style_json = json.dumps(track["style"])

            player_html = f"""
            <!doctype html>
            <html>
            <head>
            <meta charset="utf-8">
            <style>
                * {{ box-sizing: border-box; }}
                body {{
                    margin: 0;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
                    background: transparent;
                    color: #1f2933;
                }}
                .player {{
                    overflow: hidden;
                    border: 1px solid #dedbd3;
                    border-radius: 10px;
                    background: #fbfaf7;
                }}
                .lanes {{
                    position: relative;
                    height: 190px;
                    background:
                        linear-gradient(to bottom,
                            #fbfaf7 0%,
                            #fbfaf7 33.1%,
                            #ece8df 33.2%,
                            #fbfaf7 33.8%,
                            #fbfaf7 66.1%,
                            #ece8df 66.2%,
                            #fbfaf7 66.8%,
                            #fbfaf7 100%);
                    overflow: hidden;
                }}
                .lane-label {{
                    position: absolute;
                    left: 10px;
                    z-index: 3;
                    color: #90959a;
                    font-size: 9px;
                    letter-spacing: .08em;
                    text-transform: uppercase;
                }}
                .lane-label.one {{ top: 9px; }}
                .lane-label.two {{ top: 73px; }}
                .lane-label.three {{ top: 136px; }}

                .note {{
                    position: absolute;
                    height: 8px;
                    border-radius: 4px;
                    opacity: .9;
                }}
                .note.lead {{ background: #285c7a; }}
                .note.rhythm {{ background: #9d7b55; }}
                .note.low {{ background: #77808a; }}

                .cursor {{
                    position: absolute;
                    top: 0;
                    bottom: 0;
                    width: 1px;
                    background: #1f2933;
                    opacity: 0;
                    z-index: 4;
                }}

                .controls {{
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    padding: 10px;
                    border-top: 1px solid #dedbd3;
                    background: #fff;
                }}
                button {{
                    border: 1px solid #cfd3d6;
                    border-radius: 8px;
                    background: #fff;
                    color: #1f2933;
                    padding: 8px 13px;
                    cursor: pointer;
                    font: inherit;
                    font-size: 12px;
                    font-weight: 650;
                }}
                button.primary {{
                    background: #285c7a;
                    border-color: #285c7a;
                    color: #fff;
                }}
                .hint {{
                    margin-left: auto;
                    color: #8a9095;
                    font-size: 10px;
                }}
            </style>
            </head>
            <body>
                <div class="player">
                    <div class="lanes" id="lanes">
                        <div class="lane-label one">Lead</div>
                        <div class="lane-label two">Rhythm</div>
                        <div class="lane-label three">Low</div>
                        <div class="cursor" id="cursor"></div>
                    </div>
                    <div class="controls">
                        <button class="primary" onclick="playTrack()">Play</button>
                        <button onclick="stopTrack()">Stop</button>
                        <div class="hint">Browser preview</div>
                    </div>
                </div>

                <script>
                    const events = {events_json};
                    const tempo = {track["tempo"]};
                    const style = {style_json};
                    const lanes = document.getElementById("lanes");
                    const cursor = document.getElementById("cursor");
                    let audioCtx = null;
                    let active = [];
                    let cursorTimer = null;

                    const totalBeats = Math.max(...events.map(e => e.start + e.duration), 1);
                    const totalSeconds = totalBeats * (60 / tempo);

                    function laneY(role, pitch) {{
                        const top = role === "lead" ? 10 : role === "rhythm" ? 72 : 135;
                        const base = role === "low" ? 36 : role === "rhythm" ? 48 : 60;
                        const local = Math.max(0, Math.min(1, (pitch - base) / 30));
                        return top + (42 - local * 34);
                    }}

                    function drawNotes() {{
                        events.forEach(event => {{
                            event.pitches.forEach(pitch => {{
                                const el = document.createElement("div");
                                el.className = "note " + event.role;
                                el.style.left = ((event.start / totalBeats) * 100) + "%";
                                el.style.width = Math.max(0.45, (event.duration / totalBeats) * 100) + "%";
                                el.style.top = laneY(event.role, pitch) + "px";
                                lanes.appendChild(el);
                            }});
                        }});
                    }}

                    function freq(midi) {{
                        return 440 * Math.pow(2, (midi - 69) / 12);
                    }}

                    function makeDistortion(amount=30) {{
                        const n = 44100;
                        const curve = new Float32Array(n);
                        for (let i = 0; i < n; i++) {{
                            const x = i * 2 / n - 1;
                            curve[i] = ((3 + amount) * x * 20 * Math.PI / 180) /
                                (Math.PI + amount * Math.abs(x));
                        }}
                        return curve;
                    }}

                    function schedule(event, pitch, master) {{
                        const beat = 60 / tempo;
                        const start = audioCtx.currentTime + 0.06 + event.start * beat;
                        const end = start + Math.max(0.07, event.duration * beat * 0.92);
                        const velocity = Math.max(0.35, Math.min(1.1, (event.velocity || 75) / 85));

                        const osc = audioCtx.createOscillator();
                        const gain = audioCtx.createGain();
                        const filter = audioCtx.createBiquadFilter();

                        let peak = 0.06;
                        let attack = 0.015;
                        let release = 0.10;

                        if (style === "six-string sprint") {{
                            osc.type = event.role === "low" ? "square" : "sawtooth";
                            filter.type = "lowpass";
                            filter.frequency.value = event.role === "low" ? 900 : 3600;
                            peak = event.role === "rhythm" ? 0.038 : 0.06;
                            attack = 0.005;
                            release = 0.06;

                            const shaper = audioCtx.createWaveShaper();
                            shaper.curve = makeDistortion(event.role === "lead" ? 34 : 20);
                            osc.connect(gain);
                            gain.connect(filter);
                            filter.connect(shaper);
                            shaper.connect(master);
                        }} else if (style === "royal raga") {{
                            osc.type = "sine";
                            filter.type = "lowpass";
                            filter.frequency.value = event.role === "lead" ? 3000 : 1500;
                            peak = event.role === "lead" ? 0.07 : 0.03;
                            attack = event.role === "lead" ? 0.035 : 0.07;
                            release = 0.16;

                            if (event.role === "lead") {{
                                const lfo = audioCtx.createOscillator();
                                const depth = audioCtx.createGain();
                                lfo.frequency.value = 5.2;
                                depth.gain.value = 3.0;
                                lfo.connect(depth);
                                depth.connect(osc.frequency);
                                lfo.start(start);
                                lfo.stop(end);
                                active.push(lfo);
                            }}

                            osc.connect(gain);
                            gain.connect(filter);
                            filter.connect(master);
                        }} else if (style === "midnight pulse") {{
                            osc.type = event.role === "low" ? "square" : "sawtooth";
                            filter.type = "lowpass";
                            filter.frequency.value = event.role === "lead" ? 4300 : 1800;
                            peak = event.role === "lead" ? 0.055 : 0.033;
                            attack = 0.01;
                            release = 0.08;
                            osc.connect(gain);
                            gain.connect(filter);
                            filter.connect(master);
                        }} else {{
                            osc.type = event.role === "low" ? "sine" : "triangle";
                            filter.type = "lowpass";
                            filter.frequency.value = event.role === "lead" ? 3800 : 1900;
                            peak = event.role === "lead" ? 0.06 : 0.035;
                            attack = 0.012;
                            release = 0.16;
                            osc.connect(gain);
                            gain.connect(filter);
                            filter.connect(master);
                        }}

                        osc.frequency.value = freq(pitch);

                        const sustain = Math.max(start + attack + 0.01, end - release);
                        gain.gain.setValueAtTime(0.0001, start);
                        gain.gain.exponentialRampToValueAtTime(Math.max(0.001, peak * velocity), start + attack);
                        gain.gain.setValueAtTime(Math.max(0.001, peak * velocity * 0.6), sustain);
                        gain.gain.exponentialRampToValueAtTime(0.0001, end);

                        osc.start(start);
                        osc.stop(end + 0.03);
                        active.push(osc);
                    }}

                    function stopTrack() {{
                        active.forEach(node => {{ try {{ node.stop(); }} catch (e) {{}} }});
                        active = [];
                        if (cursorTimer) {{
                            clearInterval(cursorTimer);
                            cursorTimer = null;
                        }}
                        cursor.style.opacity = 0;
                        if (audioCtx) {{
                            audioCtx.close();
                            audioCtx = null;
                        }}
                    }}

                    function playTrack() {{
                        stopTrack();
                        audioCtx = new (window.AudioContext || window.webkitAudioContext)();

                        const master = audioCtx.createGain();
                        master.gain.value = 0.72;

                        const compressor = audioCtx.createDynamicsCompressor();
                        compressor.threshold.value = -18;
                        compressor.ratio.value = 4;
                        compressor.attack.value = 0.01;
                        compressor.release.value = 0.18;

                        master.connect(compressor);
                        compressor.connect(audioCtx.destination);

                        events.forEach(event => {{
                            event.pitches.forEach(pitch => schedule(event, pitch, master));
                        }});

                        const started = performance.now();
                        cursor.style.opacity = 1;
                        cursorTimer = setInterval(() => {{
                            const elapsed = (performance.now() - started) / 1000;
                            const pct = Math.min(100, (elapsed / totalSeconds) * 100);
                            cursor.style.left = pct + "%";
                            if (pct >= 100) {{
                                clearInterval(cursorTimer);
                                cursorTimer = null;
                                cursor.style.opacity = 0;
                            }}
                        }}, 30);
                    }}

                    drawNotes();
                </script>
            </body>
            </html>
            """

            components.html(player_html, height=255, scrolling=False)

            midi_path = GENERATED_DIR / track["filename"]
            if midi_path.exists():
                with midi_path.open("rb") as file:
                    st.download_button(
                        "Save MIDI file",
                        data=file.read(),
                        file_name=track["filename"],
                        mime="audio/midi",
                        use_container_width=True,
                    )

st.markdown(
    '<div class="footer-line">LumaTone · Music Generation Project</div>',
    unsafe_allow_html=True,
)
