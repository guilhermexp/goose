# Hybrid Kernel - PPPoker Automation

Automacao de PPPoker usando GPT-4o Vision + ADB.
Funciona com apps Unity que nao expoem elementos via Accessibility.

## Como Funciona

1. Captura screenshot via `adb exec-out screencap`
2. Envia para GPT-4o Vision analisar
3. GPT retorna acao (tap, type, swipe, etc) com coordenadas
4. Executa acao via ADB input
5. Repete ate completar a tarefa

## Setup

```bash
# Criar venv
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install openai

# Configurar API key
export OPENAI_API_KEY="sua-key-aqui"
```

## Uso

### Transferencia de Fichas

```bash
# Transferencia unica
python pppoker_transfer.py --agent-id 13180661 --amount 100

# Especificar clube
python pppoker_transfer.py --agent-id 13180661 --amount 100 --club "C.P.C. OnLine 2"

# Batch transfer
python pppoker_transfer.py --batch transfers_exemplo.json

# Modo teste (so abre app e descreve tela)
python pppoker_transfer.py --test
```

### Kernel Generico

```bash
# Executar qualquer tarefa
python hybrid_kernel.py "Abra o PPPoker e entre no clube C.P.C"

# Modo interativo
python hybrid_kernel.py --interactive
```

## Arquivos

- `hybrid_kernel.py` - Kernel generico para qualquer tarefa
- `pppoker_transfer.py` - Script especializado para transferencias
- `transfers_exemplo.json` - Exemplo de batch transfer
- `logs/` - Logs das execucoes

## Formato Batch Transfer

```json
[
    {"agent_id": "13180661", "amount": 100},
    {"agent_id": "12345678", "amount": 50}
]
```

## Configuracoes

No codigo voce pode ajustar:

- `MODEL_VISION` - Modelo OpenAI (default: gpt-4o)
- `MAX_STEPS` - Maximo de passos por tarefa (default: 30)
- `WAIT_AFTER_ACTION` - Espera apos cada acao (default: 3s)
- `DEFAULT_CLUB` - Clube padrao (default: C.P.C. OnLine 2)

## Troubleshooting

**Screenshot falha:**
```bash
adb devices  # Verificar conexao
adb exec-out screencap -p > test.png  # Testar manualmente
```

**App nao abre:**
```bash
adb shell am start -n com.lein.pppoker.android/com.lein.pppoker.ppsdk.app.UnityMainActivity
```

**Coordenadas erradas:**
- A resolucao esperada e 1080x2400
- Ajuste no emulador se necessario
