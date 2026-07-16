# ─── Blind Linux Kickstart - English ────────────────────────────────────────
# Main kickstart that includes blindlinux-common.ks and adds
# Blind Linux specific customizations.
# ──────────────────────────────────────────────────────────────────────────────

%include blindlinux-common.ks

# System language
lang en_US.UTF-8
keyboard us
timezone UTC

# Root password (disabled for live)
rootpw --plaintext --lock blindlinux

# ─── Packages ────────────────────────────────────────────────────────────────
%packages
%end

# ─── Post-Install: Blind Linux customizations ────────────────────────────────
%post --log=/root/ks-post-blindlinux.log
set -e

# Create live user
useradd -c "Blind Linux User" -G wheel -m blindlinux
passwd -d blindlinux > /dev/null

# Enable autologin for installed system
mkdir -p /etc/lightdm
cat >> /etc/lightdm/lightdm.conf << 'EOM'
[Seat:*]
autologin-user=blindlinux
autologin-session=mate
EOM

# Install custom sounds
mkdir -p /usr/share/blindlinux
if [ -d "/tmp/blindlinux-sounds" ]; then
    cp /tmp/blindlinux-sounds/*.mp3 /usr/share/blindlinux/ 2>/dev/null || true
fi

# Install Porta-Bop game
if [ -f "/tmp/Porta-Bop v3.0 linux.tar.gz" ]; then
    mkdir -p /usr/share/blindlinux/games
    tar -xzf "/tmp/Porta-Bop v3.0 linux.tar.gz" -C /usr/share/blindlinux/games/ 2>/dev/null || true
fi

# Create welcome script
mkdir -p /usr/local/bin
cat > /usr/local/bin/blindlinux-welcome << 'UTILITY'
#!/bin/bash
echo "=== Welcome to Blind Linux ==="
echo "This is an accessible Linux distribution."
echo "Screenreader: Orca (starts automatically)"
echo ""
echo "Quick tips:"
echo "  - Insert+Space: Open Orca preferences"
echo "  - Insert+H: Learn mode (help)"
echo "  - Insert+F: Find on screen"
echo ""
echo "Sound files are in /usr/share/blindlinux/"
echo "Porta-Bop game is in /usr/share/blindlinux/games/"
UTILITY
chmod +x /usr/local/bin/blindlinux-welcome

# Set default runlevel to graphical
systemctl set-default graphical.target

# Add user to needed groups
usermod -aG audio,video,input,bluetooth blindlinux 2>/dev/null || true

# MATE panel configuration for accessibility
mkdir -p /etc/dconf/db/local.d
cat > /etc/dconf/db/local.d/00-panel-live-user <<- EOM
[org/mate/panel/general]
object-id-list=['clock', 'menu-bar', 'volume-control', 'notification-area', 'show-desktop', 'window-list']
toplevel-id-list=['top', 'bottom']

[org/mate/panel/objects/show-desktop]
applet-iid='WnckletFactory::ShowDesktopApplet'
locked=true
object-type='applet'
position=0
toplevel-id='bottom'

[org/mate/panel/objects/window-list]
applet-iid='WnckletFactory::WindowListApplet'
locked=true
object-type='applet'
position=20
toplevel-id='bottom'

[org/mate/panel/objects/clock]
applet-iid='ClockAppletFactory::ClockApplet'
locked=true
object-type='applet'
panel-right-stick=true
position=0
toplevel-id='top'

[org/mate/panel/objects/menu-bar]
locked=true
object-type='menu-bar'
position=0
toplevel-id='top'

[org/mate/panel/objects/notification-area]
applet-iid='NotificationAreaAppletFactory::NotificationArea'
locked=true
object-type='applet'
panel-right-stick=true
position=10
toplevel-id='top'

[org/mate/panel/objects/volume-control]
applet-iid='GvcAppletFactory::GvcApplet'
locked=true
object-type='applet'
panel-right-stick=true
position=20
toplevel-id='top'
EOM
dconf update

echo "=== Blind Linux post-install complete ==="
%end

# ─── Cleanup ─────────────────────────────────────────────────────────────────
%post --log=/root/ks-cleanup.log
dnf clean all
rm -rf /tmp/* /var/tmp/*
rm -rf /var/cache/dnf/*
%end
