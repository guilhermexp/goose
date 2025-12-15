# PPPoker Automation - Estado Atual

## Data: 12/12/2025
## Status: FUNCIONAL (com limitacoes de performance)

---

## 1. O Que Foi Criado

### 1.1 MCP Server PPPoker-AutoGLM
**Arquivo**: `/android/Open-AutoGLM/mcp_server/pppoker_mcp.py`

Servidor MCP que expoe ferramentas para automacao do PPPoker usando AutoGLM.

**Ferramentas disponiveis:**
| Ferramenta | Descricao | Status |
|------------|-----------|--------|
| `pppoker_transfer` | Transfere fichas para um agente | Funcional |
| `pppoker_open_app` | Abre o PPPoker no emulador | Funcional |
| `pppoker_check_screen` | Descreve estado atual da tela | Funcional |
| `pppoker_custom_task` | Executa tarefa em linguagem natural | Funcional |
| `pppoker_batch_transfer` | Multiplas transferencias em lote | Funcional |

### 1.2 Configuracao no Claude Code
**Arquivo**: `/.mcp.json`

```json
{
  "mcpServers": {
    "android-mcp": { ... },
    "pppoker-autoglm": {
      "command": "/Users/guilhermevarela/Public/goose-fork/android/Open-AutoGLM/venv/bin/python",
      "args": ["/Users/guilhermevarela/Public/goose-fork/android/Open-AutoGLM/mcp_server/pppoker_mcp.py"],
      "env": {
        "AUTOGLM_API_KEY": "9bc888ce0ea74045b590bd1db733474d.DbvmYIblb0wZOXHo"
      }
    }
  }
}
```

### 1.3 Configuracao no Goose
**Arquivo**: `~/.config/goose/config.yaml`

```yaml
extensions:
  pppoker-autoglm:
    enabled: true
    type: stdio
    name: pppoker-autoglm
    description: AutoGLM-based automation for PPPoker chip transfers
    cmd: /Users/guilhermevarela/Public/goose-fork/android/Open-AutoGLM/venv/bin/python
    args:
      - /Users/guilhermevarela/Public/goose-fork/android/Open-AutoGLM/mcp_server/pppoker_mcp.py
    envs:
      AUTOGLM_API_KEY: 9bc888ce0ea74045b590bd1db733474d.DbvmYIblb0wZOXHo
```

### 1.4 Recipe do Goose
**Arquivo**: `~/.config/goose/recipes/pppoker-automation.json`

Recipe para iniciar sessoes pre-configuradas com:
- Extensoes pppoker-autoglm e android-mcp
- System prompt especializado em PPPoker
- Parametros: agent_id, amount, club_name

---

## 2. Arquitetura Atual

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Claude Code / Goose                               │
│                         (Usuario)                                    │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │ MCP Protocol
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   pppoker_mcp.py (MCP Server)                        │
│                                                                      │
│   Ferramentas: transfer, open_app, check_screen, custom_task, batch │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │ subprocess
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  Open-AutoGLM (main.py)                              │
│                                                                      │
│   1. Captura screenshot via ADB                                     │
│   2. Envia para API Z.AI (AutoGLM-Phone-Multilingual)               │
│   3. Recebe acao (tap, type, swipe)                                 │
│   4. Executa via ADB                                                │
│   5. Repete ate completar                                           │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │ HTTPS (API) + ADB
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│   API Z.AI                          Emulador Android                 │
│   AutoGLM-Phone-Multilingual        PPPoker App                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Testes Realizados

### 3.1 Teste Claude Code (12/12/2025 00:17)
```
> mcp__pppoker-autoglm__pppoker_open_app
✅ PPPoker aberto com sucesso!

> mcp__pppoker-autoglm__pppoker_check_screen
📱 Home screen showing CLUB section 'C.P.C. OnLin...'
   rated 2707, LOBBY, SPINUP, GLOBAL TOURNAMENT
   Menu: SHOP, FORUM, CAREER, PROFILE
```

### 3.2 Teste Transferencia (11/12/2025)
- Agente: 13180661 (Varela.teste)
- Valor: 200 fichas
- Resultado: SUCESSO
- Tempo: ~30 segundos

---

## 4. Limitacoes Atuais

### 4.1 Performance (PRINCIPAL)
**Problema**: Cada acao leva 3-5 segundos porque:
1. Screenshot capturado via ADB
2. Enviado para API Z.AI
3. Modelo processa imagem
4. Retorna coordenadas
5. Executa acao
6. Repete

**Impacto**: Uma transferencia completa leva ~30-60 segundos

### 4.2 Dependencia de Rede
- Requer conexao com API Z.AI
- Latencia adicional para cada acao

### 4.3 Custo de API
- Cada acao consome tokens da API Z.AI
- Nao temos metricas de custo ainda

### 4.4 Fragilidade
- Se a UI do PPPoker mudar, pode precisar ajustes no prompt
- Erros de rede podem interromper o fluxo

---

## 5. Melhorias Propostas

### 5.1 Curto Prazo - Workflow Hibrido
**Ideia**: Usar AutoGLM para mapear coordenadas, depois usar ADB direto

```python
# Fase 1: AutoGLM mapeia uma vez
coordenadas = autoglm_mapear_fluxo()  # Lento, mas so uma vez

# Fase 2: Execucao direta (rapida)
adb_click(coordenadas['clube'])
adb_click(coordenadas['counter'])
# etc...
```

**Beneficio**: Execucao em ~5-10 segundos em vez de 30-60

### 5.2 Medio Prazo - Cache de Coordenadas
**Ideia**: Salvar coordenadas conhecidas em arquivo

```json
{
  "resolucao": "1080x2400",
  "elementos": {
    "clube_cpc": {"x": 540, "y": 800},
    "counter": {"x": 540, "y": 2100},
    "search_member": {"x": 540, "y": 400},
    "send_button": {"x": 700, "y": 600}
  }
}
```

### 5.3 Longo Prazo - Engenharia Reversa
**Ideia**: Analisar comunicacao do PPPoker para encontrar API interna

**Opcoes**:
1. Proxy MITM para capturar requests
2. Decompilacao do APK
3. Analise de trafico de rede

**Risco**: Pode violar TOS do PPPoker

### 5.4 Alternativa - Rodar AutoGLM Local
**Ideia**: Rodar modelo na VPS (66.248.206.184) com GPU RTX A4000

**Beneficio**:
- Sem latencia de rede para API
- Sem custo por requisicao
- Mais controle

**Requisito**: INT8 quantization para caber em 16GB VRAM

---

## 6. Arquivos Importantes

| Arquivo | Descricao |
|---------|-----------|
| `/android/Open-AutoGLM/mcp_server/pppoker_mcp.py` | MCP Server |
| `/android/Open-AutoGLM/DOCUMENTACAO_AUTOGLM_PPPOKER.md` | Doc tecnica |
| `/.mcp.json` | Config Claude Code |
| `~/.config/goose/config.yaml` | Config Goose |
| `~/.config/goose/recipes/pppoker-automation.json` | Recipe Goose |
| `/android/Pppoker scripts/` | Documentacao de fluxo |

---

## 7. Credenciais

### API Z.AI
```
Key: 9bc888ce0ea74045b590bd1db733474d.DbvmYIblb0wZOXHo
URL: https://api.z.ai/api/paas/v4
Model: AutoGLM-Phone-Multilingual
```

### VPS (para deploy futuro)
```
IP: 66.248.206.184
GPU: RTX A4000 (16GB VRAM)
```

### PPPoker
```
Clube: C.P.C. OnLine 2 (ID: 3330646)
Agente teste: Varela.teste (ID: 13180661)
```

---

## 8. Proximos Passos

1. [ ] Implementar workflow hibrido (AutoGLM + ADB direto)
2. [ ] Criar cache de coordenadas por resolucao
3. [ ] Testar deploy do modelo na VPS
4. [ ] Investigar API interna do PPPoker
5. [ ] Adicionar logging/metricas de uso
6. [ ] Criar testes automatizados

---

## 9. Comandos Uteis

### Testar MCP no Claude Code
```bash
# Abrir app
mcp__pppoker-autoglm__pppoker_open_app

# Ver tela
mcp__pppoker-autoglm__pppoker_check_screen

# Transferir
mcp__pppoker-autoglm__pppoker_transfer(agent_id="13180661", amount=100)
```

### Testar AutoGLM direto
```bash
cd /Users/guilhermevarela/Public/goose-fork/android/Open-AutoGLM
source venv/bin/activate

python main.py \
  --base-url https://api.z.ai/api/paas/v4 \
  --model "AutoGLM-Phone-Multilingual" \
  --apikey "9bc888ce0ea74045b590bd1db733474d.DbvmYIblb0wZOXHo" \
  --lang en \
  "Transfer 100 chips to agent ID 13180661"
```

### Verificar emulador
```bash
adb devices
adb shell am start -n com.lein.pppoker.android/com.lein.pppoker.ppsdk.app.UnityMainActivity
```

---

**Documento criado**: 12/12/2025
**Ultima atualizacao**: 12/12/2025
**Status**: Funcional com limitacoes de performance
