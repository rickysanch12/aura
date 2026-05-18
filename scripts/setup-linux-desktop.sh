#!/bin/bash

# Setup ALCOS desktop integration for Linux

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
USER_HOME=$(eval echo ~)

echo "Setting up ALCOS desktop integration for Linux..."
echo ""

# Create applications directory
APPS_DIR="$USER_HOME/.local/share/applications"
mkdir -p "$APPS_DIR"

# Create desktop entry file
DESKTOP_FILE="$APPS_DIR/alcos.desktop"

cat > "$DESKTOP_FILE" << 'EOF'
[Desktop Entry]
Version=1.0
Name=ALCOS
Comment=Agentic Local Core OS - Autonomous AI System
Exec=${PROJECT_ROOT}/scripts/launcher.sh
Icon=application-x-executable
Terminal=false
Type=Application
Categories=Development;Utility;
EOF

# Replace PROJECT_ROOT variable
sed -i "s|\${PROJECT_ROOT}|$PROJECT_ROOT|g" "$DESKTOP_FILE"

echo "✓ Desktop shortcut created at: $DESKTOP_FILE"

# Make launcher executable
chmod +x "$PROJECT_ROOT/scripts/launcher.sh"
echo "✓ Launcher script made executable"

# Create autostart entry if requested
read -p "Enable autostart on login? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    AUTOSTART_DIR="$USER_HOME/.config/autostart"
    mkdir -p "$AUTOSTART_DIR"

    AUTOSTART_FILE="$AUTOSTART_DIR/alcos.desktop"
    cp "$DESKTOP_FILE" "$AUTOSTART_FILE"

    echo "✓ Autostart enabled"
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$APPS_DIR"
    echo "✓ Desktop database updated"
fi

echo ""
echo "Setup complete! ALCOS is now available in your applications menu."
