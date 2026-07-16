# Blind Linux

An accessible Linux distribution built on Fedora 44 with MATE desktop, based on the [vojtux](https://github.com/vojtapolasek/vojtux) approach.

## Features

- **MATE Desktop** - Lightweight, accessible desktop environment
- **Orca Screenreader** - Starts automatically at login screen and desktop
- **BRLTTY** - Braille display support
- **LightDM GTK Greeter** - Better Orca compatibility than Slick Greeter
- **PulseAudio (PipeWire)** - Audio system
- **Chromium** - Web browser
- **VLC** - Media player
- **OCR** - Tesseract + ocrmypdf
- **Custom Sounds** - Startup, login, and live session sounds
- **Porta-Bop** - Bundled audio game

## Building

Requires a Fedora 44 machine (or VM) with root access.

```bash
# Install dependencies
sudo ./build.sh deps

# Build the ISO
sudo ./build.sh build
```

The ISO will be created in the current directory.

## CI/CD

Pushes to `main`/`master` trigger a GitHub Actions build using a Fedora 44 container. The ISO is uploaded as an artifact. Tagged pushes create draft releases.

## Project Structure

```
blindlinux-common.ks        # Base kickstart (repos, packages)
blindlinux-en.ks            # English locale + customizations
build.sh                    # Build script (livemedia-creator)
.github/workflows/build.yml # CI workflow
start.mp3                   # Startup sound
logon.mp3                   # Login sound
livestart.mp3               # Live session sound
Porta-Bop v3.0 linux.tar.gz # Audio game
```
