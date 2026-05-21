#!/bin/bash

# ALCOS Desktop Launcher
# This script delegates to the comprehensive alcos-launcher script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Delegate to alcos-launcher
exec "$SCRIPT_DIR/alcos-launcher" "$@"
