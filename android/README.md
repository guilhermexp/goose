# Android Automation Projects

Projetos de automacao Android, com foco especial em PPPoker (Unity app).

## Estrutura de Pastas

```
android/
├── pppoker-automation/          # Automacao PPPoker
│   ├── hybrid-kernel/           # GPT-4o Vision + ADB (RECOMENDADO)
│   ├── autoglm/                 # AutoGLM original (lento)
│   ├── mcp-server/              # MCP Server para Goose
│   └── scripts/                 # Scripts uteis
│
├── goose-mobile-app/            # App Android do Goose
│
├── references/                  # Codigo de referencia
│   ├── android-action-kernel/   # Kernel UIAutomator
│   └── preview/                 # Preview server
│
└── docs/                        # Documentacao
```

## PPPoker Automation

### Problema
PPPoker e um app Unity - nao expoe elementos via Accessibility Services ou UIAutomator.
A unica forma de automatizar e via **screenshot + vision AI**.

### Solucoes Disponiveis

| Solucao | Velocidade | Custo | Status |
|---------|------------|-------|--------|
| **hybrid-kernel** | ~3-5s/acao | OpenAI API | **RECOMENDADO** |
| autoglm | 30-60s/acao | Z.AI API | Funciona, mas lento |
| goose-mobile-app | N/A | - | Nao funciona com Unity |

### Uso Rapido - Hybrid Kernel

```bash
cd pppoker-automation/hybrid-kernel

# Ativar venv e configurar API key
source venv/bin/activate
export OPENAI_API_KEY="sua-key"

# Testar conexao
python pppoker_transfer.py --test

# Transferir fichas
python pppoker_transfer.py --agent-id 13180661 --amount 100

# Batch transfer
python pppoker_transfer.py --batch transfers_exemplo.json
```

### Configuracoes PPPoker

- **Package**: `com.lein.pppoker.android`
- **Clube padrao**: C.P.C. OnLine 2 (ID: 3330646)
- **Agente teste**: 13180661

## Requisitos

- Android Emulator ou dispositivo conectado via ADB
- Python 3.10+
- OpenAI API Key (para hybrid-kernel)
- ADB instalado (`brew install android-platform-tools`)

## Emulador

```bash
# Listar AVDs
~/Library/Android/sdk/emulator/emulator -list-avds

# Iniciar emulador
~/Library/Android/sdk/emulator/emulator -avd Pixel_7_API_34 &

# Verificar conexao
adb devices
```
