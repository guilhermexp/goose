# Workflow de Pagamento de Rakeback - PPPoker

## Objetivo
Automatizar o envio de créditos (fichas) para agentes do clube PPPoker como pagamento de Rakeback.

---

## Dados de Entrada

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `TARGET_ID` | ID do agente que receberá o crédito | `13180661` |
| `AMOUNT` | Valor em fichas a ser enviado | `100` |

---

## Fluxo de Execução

### SESSÃO 1: Navegação para Lista de Membros
**Objetivo**: Sair do Lobby principal e abrir a ferramenta de busca de usuários.

1. **Pré-condição**: Estar na tela principal do clube (Lobby)
2. **Ação**: Clicar no ícone **"Member"** no menu inferior
3. **Resultado esperado**: Tela "Member List" aberta

**Coordenadas**:
```python
MEMBER_ICON = (x, y)  # TODO: Mapear
```

---

### SESSÃO 2: Busca e Identificação do Agente
**Objetivo**: Filtrar a lista para encontrar o usuário pelo ID.

1. Clicar na barra de pesquisa **"Search Member"**
2. Digitar o `TARGET_ID`
3. Clicar em **"OK"** ou ícone de busca
4. Clicar no resultado (faixa do usuário)

**Coordenadas**:
```python
SEARCH_BAR = (x, y)      # TODO: Mapear
SEARCH_OK = (x, y)       # TODO: Mapear
FIRST_RESULT = (x, y)    # TODO: Mapear
```

---

### SESSÃO 3: Acesso ao Menu Financeiro
**Objetivo**: Entrar na carteira do usuário.

1. **Validação**: Confirmar que o ID no topo = `TARGET_ID`
2. Clicar no botão **"Grant Credit"**

**Coordenadas**:
```python
GRANT_CREDIT_BTN = (x, y)  # TODO: Mapear
```

---

### SESSÃO 4: Execução da Transferência
**Objetivo**: Enviar as fichas.

1. Na tela "Credit", clicar no botão **"Send"** (verde, inferior esquerdo)
2. No pop-up, digitar o valor `AMOUNT`
3. Clicar em **"Confirm"**

**Coordenadas**:
```python
SEND_BTN = (x, y)        # TODO: Mapear
AMOUNT_INPUT = (x, y)    # TODO: Mapear
CONFIRM_BTN = (x, y)     # TODO: Mapear
```

---

### SESSÃO 5: Validação e Encerramento
**Objetivo**: Confirmar sucesso e sair.

1. **Validação Visual**: Nova linha com valor em verde (ex: `+100`)
2. Clicar no **"X"** ou voltar para o Lobby

**Coordenadas**:
```python
CLOSE_BTN = (x, y)  # TODO: Mapear
```

---

## Arquitetura da Solução

```
┌─────────────┐     POST /rakeback     ┌──────────────────┐
│    n8n      │ ─────────────────────► │  FastAPI Server  │
│  (trigger)  │  {target_id, amount}   │  (api_server.py) │
└─────────────┘                        └────────┬─────────┘
                                                │
                                                ▼
                                       ┌──────────────────┐
                                       │ rakeback_bot.py  │
                                       │ (workflow logic) │
                                       └────────┬─────────┘
                                                │
                                                ▼
                                       ┌──────────────────┐
                                       │   Android-MCP    │
                                       │ (UIAutomator2)   │
                                       └────────┬─────────┘
                                                │
                                                ▼
                                       ┌──────────────────┐
                                       │    Emulador      │
                                       │    PPPoker       │
                                       └──────────────────┘
```

---

## Arquivos a Criar

| Arquivo | Descrição |
|---------|-----------|
| `rakeback_bot.py` | Lógica do workflow de pagamento |
| `api_server.py` | API FastAPI para receber webhooks |
| `coords.py` | Arquivo com todas as coordenadas mapeadas |
| `utils.py` | Funções auxiliares (screenshot, validação, etc.) |

---

## Exemplo de Uso (API)

```bash
curl -X POST http://localhost:8000/rakeback \
  -H "Content-Type: application/json" \
  -d '{"target_id": "13180661", "amount": 100}'
```

**Resposta esperada**:
```json
{
  "status": "success",
  "message": "Enviado 100 fichas para 13180661",
  "timestamp": "2024-12-10T19:30:00"
}
```

---

## Próximos Passos

- [ ] Mapear coordenadas de cada elemento
- [ ] Criar `coords.py` com as coordenadas
- [ ] Implementar `rakeback_bot.py`
- [ ] Implementar `api_server.py`
- [ ] Testar fluxo completo
- [ ] Configurar webhook no n8n

---

## Notas Técnicas

- **App Unity**: PPPoker é feito em Unity, então usamos coordenadas fixas + screenshots para validação
- **Latência**: Esperar 2-3 segundos entre cada ação
- **Resolução**: Coordenadas baseadas em 1080x2400 (Pixel 7)
- **Validação**: Usar OCR ou template matching para confirmar sucesso
