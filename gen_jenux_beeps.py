"""Generate WAV files from Jenux GRUB play command patterns."""
import struct, math, wave, os

SAMPLE_RATE = 44100

def tone(freq, dur, volume=0.4, fade_ms=5):
    num_samples = int(SAMPLE_RATE * dur)
    fade_samples = int(SAMPLE_RATE * fade_ms / 1000)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        val = math.sin(2 * math.pi * freq * t) * volume
        if i < fade_samples:
            val *= i / fade_samples
        elif i > num_samples - fade_samples:
            val *= (num_samples - i) / fade_samples
        samples.append(int(max(-32767, min(32767, val * 32767))))
    return samples

def play_to_wav(name, desc, notes):
    """notes = [(freq_hz, duration_seconds), ...]"""
    samples = []
    for freq, dur in notes:
        if freq <= 20:
            samples += [0] * int(SAMPLE_RATE * dur)
        else:
            samples += tone(freq, dur)
        samples += [0] * int(SAMPLE_RATE * 0.01)
    path = os.path.join(out_dir, f"{name}.wav")
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(struct.pack(f'<{len(samples)}h', *samples))
    total_dur = len(samples) / SAMPLE_RATE
    print(f"{name}: {desc} ({total_dur:.1f}s)")
    print(f"  -> {path}")

out_dir = r'C:\Users\natan\projects\blinbuntu\jenux_beeps'
os.makedirs(out_dir, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. Empire Strikes Back melody (from Jenux EFI GRUB config)
#    GRUB: play 1750 523 1 392 1 523 1 659 1 784 1 1047 1 784 1 415 1 523 1
#          622 1 831 1 622 1 831 1 1046 1 1244 1 1661 1 1244 1 466 1 587 1
#          698 1 932 1 1175 1 1397 1 1865 1 1397 1
#    Opening: 1750Hz sustained, then melody notes each ~0.18s
# ═══════════════════════════════════════════════════════════════════════════════
empire_notes = [
    (1750, 1.2),
    (523, 0.18), (392, 0.18), (523, 0.18), (659, 0.18),
    (784, 0.18), (1047, 0.18), (784, 0.18),
    (415, 0.18), (523, 0.18), (622, 0.18), (831, 0.25),
    (622, 0.18), (831, 0.18), (1046, 0.18), (1244, 0.18),
    (1661, 0.25), (1244, 0.18),
    (466, 0.18), (587, 0.18), (698, 0.18), (932, 0.18),
    (1175, 0.18), (1397, 0.18), (1865, 0.3), (1397, 0.3),
]
play_to_wav("jenux1_empire_strikes_back", "Empire Strikes Back - EFI boot melody", empire_notes)

# Faster version
empire_fast = [(1750, 0.8)]
for f, d in empire_notes[1:]:
    empire_fast.append((f, d * 0.7))
play_to_wav("jenux2_empire_fast", "Empire Strikes Back - faster version", empire_fast)

# Slower version
empire_slow = [(1750, 2.0)]
for f, d in empire_notes[1:]:
    empire_slow.append((f, d * 1.4))
play_to_wav("jenux3_empire_slow", "Empire Strikes Back - slower version", empire_slow)

# ═══════════════════════════════════════════════════════════════════════════════
# 2. Legacy BIOS boot sound
#    GRUB: play 600 294 5 277 2 330 4 294 5
#    Interpreted as ascending/descending tones
# ═══════════════════════════════════════════════════════════════════════════════
bios_notes = [
    (294, 0.35), (277, 0.15), (330, 0.3), (294, 0.35),
]
play_to_wav("jenux4_bios_boot", "Legacy BIOS boot sound", bios_notes)

# With opening tone
bios_with_intro = [
    (600, 0.5),
    (294, 0.35), (277, 0.15), (330, 0.3), (294, 0.35),
]
play_to_wav("jenux5_bios_with_intro", "BIOS boot with 600Hz intro", bios_with_intro)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. Status beeps (from Jenux GRUB config)
#    "no/default" = 440Hz, "yes/enabled" = 880Hz
# ═══════════════════════════════════════════════════════════════════════════════
play_to_wav("jenux6_status_low", "Status beep LOW (440Hz) - default/off", [(440, 0.5)])
play_to_wav("jenux7_status_high", "Status beep HIGH (880Hz) - enabled/on", [(880, 0.5)])

# ═══════════════════════════════════════════════════════════════════════════════
# 4. Kernel loading sequence beeps
#    Various pitches indicating boot progress
# ═══════════════════════════════════════════════════════════════════════════════
kernel_load = [
    (250, 0.15), (440, 0.3),
    (150, 0.1),
    (300, 0.15),
    (450, 0.15),
    (600, 0.15),
    (480, 0.1), (440, 0.3),
]
play_to_wav("jenux8_kernel_load", "Kernel loading sequence beeps", kernel_load)

# ═══════════════════════════════════════════════════════════════════════════════
# 5. Config found / not found
#    GRUB: play 400 523 2 392 1 392 1 440 2 392 2 1 2 494 2 523 2 (found)
#          play 500 500 1 / play 250 250 1 (not found)
# ═══════════════════════════════════════════════════════════════════════════════
config_found = [
    (523, 0.2), (392, 0.1), (392, 0.1), (440, 0.2),
    (392, 0.2), (494, 0.2), (523, 0.3),
]
play_to_wav("jenux9_config_found", "Config file found melody", config_found)

config_notfound = [
    (500, 0.3), (250, 0.3),
]
play_to_wav("jenux10_config_notfound", "Config file NOT found", config_notfound)

# ═══════════════════════════════════════════════════════════════════════════════
# 6. Welcome chime (combined)
# ═══════════════════════════════════════════════════════════════════════════════
welcome = [
    (523, 0.2), (659, 0.2), (784, 0.2), (1047, 0.4),
    (784, 0.15), (1047, 0.5),
]
play_to_wav("jenux11_welcome", "Welcome chime (ascending major)", welcome)

print("\nDone! Listen to these and tell me which ones you want to use.")
