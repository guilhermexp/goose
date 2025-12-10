# Integração Android Preview no Goose

## Visão Geral

Integrar um preview em tempo real do emulador Android dentro da interface do Goose, permitindo visualizar as ações do agente enquanto ele opera o dispositivo.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              GOOSE APP                                  │
├────────────────────────────────────┬────────────────────────────────────┤
│                                    │                                    │
│           GOOSE CHAT               │       ANDROID PREVIEW              │
│                                    │                                    │
│  ┌──────────────────────────────┐  │  ┌──────────────────────────────┐  │
│  │ What would you like to       │  │  │   ┌────────────────────┐    │  │
│  │ work on?                     │  │  │   │                    │    │  │
│  │                              │  │  │   │    PPPoker App     │    │  │
│  │ > Enviar 100 fichas para     │  │  │   │                    │    │  │
│  │   agente 13180661            │  │  │   │   [Live Preview]   │    │  │
│  │                              │  │  │   │                    │    │  │
│  │ [Executando workflow...]     │  │  │   │                    │    │  │
│  │ ✓ Abrindo Members            │  │  │   └────────────────────┘    │  │
│  │ ✓ Buscando ID 13180661       │  │  │                              │  │
│  │ ○ Enviando crédito...        │  │  │   [Controles do Emulador]    │  │
│  └──────────────────────────────┘  │  └──────────────────────────────┘  │
│                                    │                                    │
├────────────────────────────────────┴────────────────────────────────────┤
│  [SHOP] [FORUM] [CAREER] [PROFILE] │ Status: Conectado | FPS: 30       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Arquitetura Proposta

### Stack Tecnológica

```
ui/desktop/
├── src/
│   ├── components/
│   │   ├── AndroidPreview/          # NOVO - Componente do preview
│   │   │   ├── AndroidPreview.tsx   # Componente principal
│   │   │   ├── EmulatorControls.tsx # Botões (back, home, etc)
│   │   │   ├── ScreenCapture.tsx    # Captura de tela
│   │   │   └── ConnectionStatus.tsx # Status da conexão
│   │   └── Layout/
│   │       └── SplitLayout.tsx      # Layout com 2 painéis
│   ├── hooks/
│   │   └── useAndroidDevice.ts      # Hook para controle do device
│   └── services/
│       └── android/
│           ├── adb.ts               # Wrapper ADB
│           ├── scrcpy.ts            # Integração scrcpy
│           └── screenshot.ts        # Screenshot streaming
```

---

## Opções de Implementação do Preview

### Opção 1: Screenshots em Tempo Real (Recomendado para MVP)

**Como funciona:**
- Backend captura screenshots via ADB a cada 100-200ms
- Envia via WebSocket para o frontend
- Frontend renderiza como `<img>` ou `<canvas>`

**Prós:** Simples, funciona em qualquer plataforma
**Contras:** Latência maior (200-500ms), não é video real

```typescript
// screenshot.ts
export async function captureScreen(deviceId: string): Promise<Buffer> {
  const { execSync } = require('child_process');
  return execSync(`adb -s ${deviceId} exec-out screencap -p`);
}

// Loop de captura
setInterval(async () => {
  const screenshot = await captureScreen('emulator-5554');
  websocket.send(screenshot);
}, 200);
```

### Opção 2: scrcpy Embutido

**Como funciona:**
- scrcpy roda como processo filho
- Captura janela do scrcpy via Electron
- Ou usa scrcpy em modo socket/v4l2

**Prós:** Video fluido em 60fps
**Contras:** Mais complexo, dependência externa

```typescript
// scrcpy.ts
import { spawn } from 'child_process';

export function startScrcpy(deviceId: string) {
  return spawn('scrcpy', [
    '-s', deviceId,
    '--window-title', 'Android Preview',
    '--window-borderless',
    '--max-size', '400'
  ]);
}
```

### Opção 3: WebRTC (Avançado)

**Como funciona:**
- Servidor WebRTC no backend
- Stream de video via navegador
- Baixa latência

**Prós:** Latência muito baixa
**Contras:** Complexidade alta

---

## Integração com Android-MCP

### Como Extensão MCP do Goose

```yaml
# ~/.config/goose/extensions.yaml
extensions:
  android-mcp:
    name: "Android MCP"
    command: "uv"
    args: ["--directory", "/path/to/Android-MCP", "run", "main.py", "--emulator"]
    env:
      DEVICE_ID: "emulator-5554"
```

### Tools Disponíveis no Goose

Quando o Android-MCP estiver conectado como extensão:

| Tool | Descrição |
|------|-----------|
| `android_state` | Captura estado da tela + elementos |
| `android_click` | Clica em coordenadas (x, y) |
| `android_type` | Digita texto |
| `android_swipe` | Faz gestos de swipe |
| `android_press` | Pressiona botões (back, home) |
| `android_screenshot` | Captura screenshot |

---

## Estrutura do Monorepo

```
goose-fork/
├── ui/
│   └── desktop/           # App Electron existente
├── crates/                # Backend Rust existente
├── android/               # NOVO - Módulo Android
│   ├── mcp-server/        # Android-MCP server
│   ├── preview/           # Serviço de preview
│   └── emulator/          # Scripts para gerenciar emulador
├── recipes/
│   └── rakeback.yaml      # Recipe de pagamento Rakeback
└── ANDROID_INTEGRATION.md # Este documento
```

---

## Implementação - Fases

### Fase 1: MVP (Screenshots)
- [ ] Criar componente `AndroidPreview.tsx`
- [ ] Implementar captura de screenshots via IPC
- [ ] Adicionar toggle para mostrar/esconder preview
- [ ] Integrar Android-MCP como extensão

### Fase 2: Controles
- [ ] Adicionar botões de controle (back, home, volume)
- [ ] Permitir clique no preview (envia para device)
- [ ] Status de conexão do device

### Fase 3: Polish
- [ ] Migrar para scrcpy (video fluido)
- [ ] Múltiplos devices
- [ ] Gravar sessões

---

## Componente React - AndroidPreview.tsx

```tsx
// src/components/AndroidPreview/AndroidPreview.tsx
import React, { useEffect, useState } from 'react';
import { useAndroidDevice } from '../../hooks/useAndroidDevice';

interface AndroidPreviewProps {
  deviceId?: string;
  width?: number;
  refreshRate?: number;
}

export const AndroidPreview: React.FC<AndroidPreviewProps> = ({
  deviceId = 'emulator-5554',
  width = 300,
  refreshRate = 200
}) => {
  const { screenshot, isConnected, error } = useAndroidDevice(deviceId, refreshRate);

  if (error) {
    return (
      <div className="android-preview-error">
        <p>Erro: {error}</p>
        <button onClick={() => window.electron.startEmulator()}>
          Iniciar Emulador
        </button>
      </div>
    );
  }

  if (!isConnected) {
    return (
      <div className="android-preview-loading">
        <p>Conectando ao dispositivo...</p>
      </div>
    );
  }

  return (
    <div className="android-preview">
      <div className="android-preview-header">
        <span className="status-dot connected" />
        <span>Android - {deviceId}</span>
      </div>
      <img
        src={`data:image/png;base64,${screenshot}`}
        alt="Android Preview"
        width={width}
        className="android-screen"
      />
      <div className="android-controls">
        <button onClick={() => window.electron.androidPress('back')}>◀</button>
        <button onClick={() => window.electron.androidPress('home')}>○</button>
        <button onClick={() => window.electron.androidPress('recent')}>□</button>
      </div>
    </div>
  );
};
```

---

## Recipe de Rakeback

```yaml
# recipes/rakeback.yaml
name: "Pagamento de Rakeback PPPoker"
description: "Envia créditos para agentes no PPPoker"
version: "1.0.0"

inputs:
  - name: target_id
    description: "ID do agente"
    type: string
    required: true
  - name: amount
    description: "Valor em fichas"
    type: number
    required: true

extensions:
  - android-mcp

steps:
  - name: "Verificar conexão"
    action: android_state
    validate: "device_connected == true"

  - name: "Navegar para Members"
    action: android_click
    params:
      x: 168
      y: 1107
    wait: 2000

  - name: "Buscar membro"
    action: android_type
    params:
      text: "{{target_id}}"
    wait: 1000

  # ... continua com os passos do workflow

outputs:
  - name: success
    type: boolean
  - name: transaction_id
    type: string
```

---

## Próximos Passos

1. **Decisão**: Qual opção de preview usar? (Screenshots recomendado para MVP)
2. **Setup**: Copiar Android-MCP para `android/mcp-server/`
3. **Desenvolver**: Componente `AndroidPreview.tsx`
4. **Integrar**: Android-MCP como extensão do Goose
5. **Testar**: Fluxo completo de Rakeback
6. **Recipe**: Criar recipe reutilizável

---

## Comandos Úteis

```bash
# Iniciar emulador
~/Library/Android/sdk/emulator/emulator -avd Pixel_7_API_34 &

# Verificar conexão
adb devices

# Screenshot manual
adb exec-out screencap -p > screen.png

# Iniciar Goose (dev)
cd ui/desktop && npm run start-gui
```
