#!/bin/bash
# Script para iniciar o ambiente Android completo para o Goose

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ANDROID_DIR="$(dirname "$SCRIPT_DIR")"
GOOSE_DIR="$(dirname "$ANDROID_DIR")"

echo "=============================================="
echo "  Goose Android Environment"
echo "=============================================="

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar ADB
if ! command -v adb &> /dev/null; then
    echo -e "${RED}Erro: ADB não encontrado${NC}"
    echo "Instale com: brew install --cask android-platform-tools"
    exit 1
fi

# Verificar emulador
EMULATOR_PATH="$HOME/Library/Android/sdk/emulator/emulator"
if [ ! -f "$EMULATOR_PATH" ]; then
    echo -e "${RED}Erro: Emulador não encontrado${NC}"
    echo "Instale o Android Studio e configure um AVD"
    exit 1
fi

# Verificar uv
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Erro: uv não encontrado${NC}"
    echo "Instale com: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Listar AVDs disponíveis
echo -e "${YELLOW}AVDs disponíveis:${NC}"
$EMULATOR_PATH -list-avds

# Verificar se há dispositivos conectados
DEVICES=$(adb devices | grep -v "List" | grep "device" | wc -l)

if [ "$DEVICES" -eq 0 ]; then
    echo -e "${YELLOW}Nenhum dispositivo conectado. Iniciando emulador...${NC}"

    # Usar o primeiro AVD disponível
    AVD=$($EMULATOR_PATH -list-avds | head -1)
    if [ -z "$AVD" ]; then
        echo -e "${RED}Erro: Nenhum AVD configurado${NC}"
        exit 1
    fi

    echo -e "${GREEN}Iniciando AVD: $AVD${NC}"
    $EMULATOR_PATH -avd "$AVD" -no-snapshot-load &

    # Aguardar emulador ficar pronto
    echo "Aguardando emulador iniciar..."
    adb wait-for-device
    sleep 10
    echo -e "${GREEN}Emulador iniciado!${NC}"
else
    echo -e "${GREEN}Dispositivo já conectado${NC}"
fi

# Mostrar dispositivos
echo ""
echo -e "${YELLOW}Dispositivos conectados:${NC}"
adb devices -l

# Iniciar servidor de preview
echo ""
echo -e "${YELLOW}Iniciando servidor de preview...${NC}"
cd "$ANDROID_DIR/preview"

# Instalar dependências se necessário
if [ ! -d ".venv" ]; then
    echo "Instalando dependências..."
    uv sync
fi

# Iniciar servidor
echo -e "${GREEN}Iniciando Android Preview Server em http://localhost:8765${NC}"
uv run python server.py &
PREVIEW_PID=$!

echo ""
echo "=============================================="
echo -e "${GREEN}Ambiente Android pronto!${NC}"
echo "=============================================="
echo ""
echo "Endpoints:"
echo "  - Preview API: http://localhost:8765"
echo "  - WebSocket:   ws://localhost:8765/ws/<device_id>"
echo ""
echo "Para parar: kill $PREVIEW_PID"
echo ""

# Manter script rodando
wait $PREVIEW_PID
