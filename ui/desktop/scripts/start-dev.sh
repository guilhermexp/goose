#!/bin/bash
# Start development environment: Android Emulator + Goose

echo "🚀 Iniciando ambiente de desenvolvimento..."

# Kill any existing processes
pkill -f "qemu-system" 2>/dev/null
pkill -f "Electron" 2>/dev/null
sleep 2

# Start Android Emulator in background
echo "📱 Iniciando Android Emulator..."
~/Library/Android/sdk/emulator/emulator -avd Pixel_7_API_34 -no-snapshot-load &
EMULATOR_PID=$!

# Wait for emulator to start
echo "⏳ Aguardando emulador iniciar..."
sleep 10

# Start Goose
echo "🪿 Iniciando Goose..."
cd "$(dirname "$0")/.." && npm run start-gui
