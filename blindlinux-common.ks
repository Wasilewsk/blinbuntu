# ─── Blind Linux Kickstart - Common ─────────────────────────────────────────
# Based on vojtux approach, adapted for Blind Linux.
# Fedora 44, MATE desktop, accessibility-first.
# ──────────────────────────────────────────────────────────────────────────────

# Repositories
repo --name=fedora --mirrorlist=https://mirrors.fedoraproject.org/mirrorlist?repo=fedora-44&arch=x86_64
repo --name=updates --mirrorlist=https://mirrors.fedoraproject.org/mirrorlist?repo=updates-released-f44&arch=x86_64
url --mirrorlist=https://mirrors.fedoraproject.org/mirrorlist?repo=fedora-44&arch=x86_64

# RPM Fusion repos (for VLC, multimedia, etc.)
repo --name=rpmfusion-free --mirrorlist=https://mirrors.rpmfusion.org/metalink?repo=free-fedora-44&arch=x86_64
repo --name=rpmfusion-free-updates --mirrorlist=https://mirrors.rpmfusion.org/metalink?repo=free-fedora-updates-released-44&arch=x86_64
repo --name=rpmfusion-nonfree --mirrorlist=https://mirrors.rpmfusion.org/metalink?repo=nonfree-fedora-44&arch=x86_64
repo --name=rpmfusion-nonfree-updates --mirrorlist=https://mirrors.rpmfusion.org/metalink?repo=nonfree-fedora-updates-released-44&arch=x86_64

# SELinux permissive
selinux --permissive

# brltty group
group --name brlapi

# Services
services --enabled="chronyd,brltty"

# Disk
part / --size 10240 --fstype ext4

# ─── Packages ────────────────────────────────────────────────────────────────
%packages
# Base
@core
kernel
dracut-live

# Desktop
@mate-desktop
@mate-applications
@input-methods

# Hardware support
@hardware-support
gutenprint-cups
cups-filters
foomatic-db
foomatic-db-ppds
splix
hplip
xorg-x11-drv-nouveau
libsane-hpaio

# Audio
pipewire-pulseaudio
pavucontrol
alsa-utils
sox
audacity
soundconverter
timidity++

# Accessibility
orca
espeak-ng
brltty
brltty-xw
speech-dispatcher-utils
a11y-sound-theme

# Display manager (lightdm-gtk-greeter for Orca compatibility)
-slick-greeter
-slick-greeter-mate
lightdm-gtk-greeter
lightdm-gtk-greeter-settings

# OCR
tesseract-langpack-eng
ocrmypdf

# Software
chromium
vlc
pidgin
xsane
git
curl
wget
sed
nano
tmux
unrar
ifuse
jmtpfs
pandoc

# Firmware
linux-firmware

# Fonts
dejavu-sans-fonts
dejavu-serif-fonts
google-noto-sans-fonts
google-noto-serif-fonts

# Tools
vim
less
%end

# ─── Post-Install: Live session setup ────────────────────────────────────────
%post --log=/root/ks-post-live.log
# set livesys session type
sed -i 's/^livesys_session=.*/livesys_session="mate"/' /etc/sysconfig/livesys

# configure speech dispatcher to use espeak-ng
sed -i 's/#AddModule "espeak-ng"                "sd_espeak-ng" "espeak-ng.conf"/AddModule "espeak-ng"                "sd_espeak-ng" "espeak-ng.conf"/' /etc/speech-dispatcher/speechd.conf

# setup lightdm - Orca starts at login screen
mkdir -p /usr/local/bin
cat > /usr/local/bin/orca-login-wrapper << 'EOM'
#!/bin/bash
amixer -c 0 set Master playback 50% unmute
/usr/bin/orca &
EOM
chmod 755 /usr/local/bin/orca-login-wrapper

mkdir -p /etc/lightdm
cat >> /etc/lightdm/lightdm-gtk-greeter.conf << 'EOM'
[greeter]
background = /usr/share/backgrounds/default.png
reader = /usr/local/bin/orca-login-wrapper
a11y-states = +reader
EOM
%end
