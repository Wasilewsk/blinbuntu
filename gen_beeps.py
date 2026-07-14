import struct, math, wave, os

SAMPLE_RATE = 44100

def tone(freqs, dur, volume=0.35, fade_ms=5, vibrato=0):
    num_samples = int(SAMPLE_RATE * dur)
    fade_samples = int(SAMPLE_RATE * fade_ms / 1000)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        val = 0
        for f in freqs:
            v = f + vibrato * math.sin(2 * math.pi * 5.5 * t) if vibrato else f
            val += math.sin(2 * math.pi * v * t)
        val = (val / len(freqs)) * volume
        if i < fade_samples:
            val *= i / fade_samples
        elif i > num_samples - fade_samples:
            val *= (num_samples - i) / fade_samples
        samples.append(int(max(-32767, min(32767, val * 32767))))
    return samples

def seq(notes):
    """notes = [(freq, dur), ...]"""
    out = []
    for f, d in notes:
        if f == 0:
            out += silence(d)
        else:
            out += tone([f], d)
        out += silence(0.01)
    return out

def chords(chords_list):
    """chords_list = [([freqs], dur), ...]"""
    out = []
    for freqs, d in chords_list:
        out += tone(freqs, d, fade_ms=20, vibrato=2)
        out += silence(0.03)
    return out

def silence(dur):
    return [0] * int(SAMPLE_RATE * dur)

def concat(*blocks):
    return [s for b in blocks for s in s if isinstance(s, list)]

def cat(*blocks):
    result = []
    for b in blocks:
        result.extend(b)
    return result

out_dir = r'C:\Users\natan\projects\blinbuntu\beep_samples'
os.makedirs(out_dir, exist_ok=True)
beeps = []

# ── Mario Coin Sound (longer, more resonant) ──
coin = cat(
    tone([987.77], 0.08, volume=0.4),
    silence(0.02),
    tone([1318.51], 0.25, volume=0.4, fade_ms=3),
    silence(0.05),
    tone([1318.51, 1975.53], 0.3, volume=0.3, fade_ms=30),
)
beeps.append(("mario1_coin", coin, "Mario coin - B5 then E6 with harmonic ring"))

# ── Mario 1-UP (6 notes ascending, longer) ──
oneup = cat(
    silence(0.05),
    tone([330.0], 0.10),   # E5
    silence(0.02),
    tone([392.0], 0.10),   # G5
    silence(0.02),
    tone([523.3], 0.10),   # C6
    silence(0.02),
    tone([659.3], 0.10),   # E6
    silence(0.02),
    tone([784.0], 0.10),   # G6
    silence(0.02),
    tone([1046.5], 0.25),  # C7
    silence(0.1),
    tone([1046.5, 1568.0], 0.4, volume=0.25, fade_ms=40),  # ring out
)
beeps.append(("mario2_1up", oneup, "Mario 1-UP - 6-note ascending with ring"))

# ── Mario Power-Up (ascending arpeggio with bass) ──
powerup = cat(
    silence(0.05),
    tone([196.0], 0.08),   # G4
    silence(0.01),
    tone([261.6], 0.08),   # C5
    silence(0.01),
    tone([329.6], 0.08),   # E5
    silence(0.01),
    tone([392.0], 0.08),   # G5
    silence(0.01),
    tone([523.3], 0.08),   # C6
    silence(0.01),
    tone([659.3], 0.08),   # E6
    silence(0.01),
    tone([784.0], 0.15),   # G6
    silence(0.01),
    tone([1046.5], 0.40),  # C7 sustained
    silence(0.05),
    tone([523.3, 784.0, 1046.5], 0.5, volume=0.25, fade_ms=40, vibrato=3),  # C major chord
)
beeps.append(("mario3_powerup", powerup, "Mario Power-Up - ascending arpeggio to C chord"))

# ── Mario Level Complete (victory fanfare) ──
victory = cat(
    silence(0.05),
    # Phrase 1: ascending
    tone([523.3], 0.15), silence(0.02),   # C6
    tone([523.3], 0.15), silence(0.02),   # C6
    tone([523.3], 0.15), silence(0.02),   # C6
    tone([392.0], 0.15), silence(0.02),   # G5
    tone([523.3], 0.15), silence(0.02),   # C6
    tone([659.3], 0.35),                   # E6 sustained
    silence(0.1),
    # Phrase 2: resolution
    tone([659.3], 0.15), silence(0.02),   # E6
    tone([659.3], 0.15), silence(0.02),   # E6
    tone([659.3], 0.15), silence(0.02),   # E6
    tone([523.3], 0.15), silence(0.02),   # C6
    tone([659.3], 0.15), silence(0.02),   # E6
    tone([784.0], 0.50),                   # G6 sustained
    silence(0.15),
    # Final chord
    tone([523.3, 659.3, 784.0, 1046.5], 0.8, volume=0.3, fade_ms=50, vibrato=3),
)
beeps.append(("mario4_victory", victory, "Mario Level Complete fanfare, ~4s"))

# ── Mario Game Over (descending sad) ──
gameover = cat(
    silence(0.05),
    tone([392.0], 0.25), silence(0.02),   # G5
    tone([329.6], 0.25), silence(0.02),   # E5
    tone([261.6], 0.25), silence(0.02),   # C5
    tone([220.0], 0.25), silence(0.02),   # A4
    tone([196.0], 0.25), silence(0.02),   # G4
    tone([164.8], 0.25), silence(0.02),   # E4
    tone([130.8], 0.50),                   # C4 sustained
    silence(0.1),
    tone([130.8, 164.8], 0.6, volume=0.25, fade_ms=50, vibrato=2),
)
beeps.append(("mario5_gameover", gameover, "Mario Game Over - descending minor, ~3s"))

# ── Mario Star Power (fast repeating arpeggio) ──
star = cat(
    silence(0.05),
)
for _ in range(4):
    star += cat(
        tone([329.6], 0.06), silence(0.01),
        tone([493.9], 0.06), silence(0.01),
        tone([659.3], 0.06), silence(0.01),
        tone([987.8], 0.06), silence(0.01),
        tone([659.3], 0.06), silence(0.01),
        tone([493.9], 0.06), silence(0.01),
    )
star += tone([659.3, 987.8], 0.5, volume=0.3, fade_ms=40, vibrato=5)
beeps.append(("mario6_star", star, "Mario Star Power - fast arpeggio x4 + sustain"))

# ── Boot Jingle (original, Mario-inspired, 5s) ──
boot = cat(
    silence(0.1),
    # Opening chord
    chords([([261.6, 329.6, 392.0], 0.5)]),
    silence(0.08),
    # Ascending melody
    seq([(392.0, 0.15), (440.0, 0.15), (493.9, 0.15), (523.3, 0.3)]),
    silence(0.08),
    # Higher phrase
    seq([(659.3, 0.2), (587.3, 0.15), (523.3, 0.15), (493.9, 0.2)]),
    silence(0.08),
    # Descending resolution
    seq([(440.0, 0.15), (392.0, 0.15), (349.2, 0.15), (329.6, 0.3)]),
    silence(0.08),
    # Final ascending push
    seq([(392.0, 0.12), (493.9, 0.12), (587.3, 0.12), (659.3, 0.12), (784.0, 0.12)]),
    silence(0.05),
    # Final sustained chord
    chords([([261.6, 329.6, 392.0, 523.3], 1.0)]),
)
beeps.append(("mario7_boot_jingle", boot, "Original boot jingle, Mario-inspired, ~5s"))

for name, samples, desc in beeps:
    path = os.path.join(out_dir, f"{name}.wav")
    dur = len(samples) / SAMPLE_RATE
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(struct.pack(f'<{len(samples)}h', *samples))
    print(f"{name}: {desc} ({dur:.1f}s)")
    print(f"  -> {path}")
