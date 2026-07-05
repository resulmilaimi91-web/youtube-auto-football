import numpy as np


def generate_kids_background(duration_sec, sample_rate=44100):
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 349.23, 329.63]
    music = np.zeros_like(t)
    note_len = int(sample_rate * (duration_sec / len(notes)))
    for i, freq in enumerate(notes):
        start = i * note_len
        end = min(start + note_len, len(t))
        if start >= len(t):
            break
        seg = t[start:end] - t[start]
        env = np.exp(-seg * 2)
        note = np.sin(2 * np.pi * freq * seg) * env
        note += 0.3 * np.sin(2 * np.pi * freq * 2 * seg) * env
        fade_len = min(400, len(note) // 4)
        note[:fade_len] *= np.linspace(0, 1, fade_len)
        note[-fade_len:] *= np.linspace(1, 0, fade_len)
        music[start:end] += note * 0.15
    chords = [261.63 + 329.63 + 392.00, 293.66 + 349.23 + 440.00, 329.63 + 392.00 + 349.23, 261.63 + 329.63 + 392.00]
    chord_len = int(sample_rate * (duration_sec / len(chords)))
    for i, chord in enumerate(chords):
        start = i * chord_len
        end = min(start + chord_len, len(t))
        if start >= len(t):
            break
        seg = t[start:end] - t[start]
        chord_wave = sum(np.sin(2 * np.pi * f * seg) for f in [261.63, 329.63, 392.00])
        chord_wave *= 0.5 * np.exp(-seg * 1.5)
        fade_len = min(800, len(chord_wave) // 3)
        chord_wave[:fade_len] *= np.linspace(0, 1, fade_len)
        music[start:end] += chord_wave * 0.08
    max_val = np.max(np.abs(music))
    if max_val > 0:
        music = music / max_val * 0.08
    music_16bit = (music * 32767).astype(np.int16)
    import wave
    import tempfile
    temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    with wave.open(temp.name, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(music_16bit.tobytes())
    return temp.name
