# Workflow Template: Transferência de Fichas PPPoker

## Parâmetros
- **clube_nome**: Nome do clube (ex: C.P.C. OnLine 2)
- **agente_id**: ID do agente de 8 dígitos (ex: 13180661)
- **valor_transferencia**: Valor em fichas a transferir (ex: 100)

## Passos Programáticos

### 1. Abrir Aplicativo
```python
action = "click"
element = "PPPoker app icon"
wait_after = 3
validation = "Version text visible"
```

### 2. Selecionar Clube
```python
action = "click"
element = f"Club card with name '{clube_nome}'"
wait_after = 2
validation = "Club tabs visible (TONGITS, TEEN PATTI, etc)"
```

### 3. Abrir Counter
```python
action = "click"
element = "Counter icon (3rd icon in bottom navigation)"
wait_after = 2
validation = "Counter modal with Trade/Send Items/Ticket tabs"
```

### 4. Buscar Agente
```python
action = "click"
element = "Search Member input field"
wait_after = 1
validation = "Keyboard visible and field focused"
```

### 5. Inserir ID
```python
action = "type"
text = agente_id
method_alternative = "click on suggestion if available"
wait_after = 1
validation = f"Search results showing agent with ID {agente_id}"
```

### 6. Selecionar Resultado
```python
action = "click"
element = f"Member result card for ID {agente_id}"
wait_after = 1
validation = "Green checkmark appears next to selected agent"
```

### 7. Clicar Send
```python
action = "click"
element = "Send button (green)"
wait_after = 2
validation = "Send modal with numeric keypad visible"
```

### 8. Digitar Valor
```python
action = "type_numeric"
value = valor_transferencia
method = "click numeric keypad buttons"
digits = str(valor_transferencia)
for digit in digits:
    click(f"number {digit} button")
wait_after = 1
validation = f"Amount field shows {valor_transferencia}"
```

### 9. Confirmar Valor
```python
action = "click"
element = "Checkmark button on numeric keypad"
wait_after = 2
validation = f"Confirmation screen with 'Total: {valor_transferencia}'"
```

### 10. Validar e Confirmar
```python
# Validação pré-confirmação
assert amount_displayed == valor_transferencia
assert agent_id_displayed == agente_id

action = "click"
element = "Confirm button (green)"
wait_after = 2
validation = "Success message appears"
```

### 11. Fechar Modal
```python
action = "click"
element = "X close button in Counter modal header"
wait_after = 1
validation = "Back to club main screen"
```

## Validações Finais
```python
# Verificar atualização de saldos
balance_decreased = initial_balance - valor_transferencia
agent_balance_increased = agent_initial_balance + valor_transferencia

assert current_balance == balance_decreased
assert success_message_shown == True
```

## Estrutura de Dados

```python
class PPPokerTransfer:
    def __init__(self, club_name, agent_id, amount):
        self.club_name = club_name
        self.agent_id = agent_id
        self.amount = amount
        self.initial_balance = None
        self.final_balance = None
        self.agent_initial_balance = None
        self.agent_final_balance = None
        self.success = False
        
    def execute(self):
        # Passo 1: Abrir app
        self.open_app()
        
        # Passo 2: Entrar no clube
        self.select_club(self.club_name)
        
        # Passo 3: Abrir Counter
        self.open_counter()
        
        # Passo 4-6: Buscar e selecionar agente
        self.search_agent(self.agent_id)
        
        # Passo 7-9: Enviar valor
        self.send_amount(self.amount)
        
        # Passo 10: Confirmar
        self.confirm_transfer()
        
        # Passo 11: Fechar
        self.close_modal()
        
        return self.success
```

## Seletores de Elementos

```python
SELECTORS = {
    "app_icon": "PPPoker app icon",
    "club_card": lambda name: f"Club card with name '{name}'",
    "counter_icon": "Counter icon in bottom navigation menu, third icon from left",
    "search_field": "Search Member text input field",
    "member_result": lambda id: f"Member result with ID {id}",
    "send_button": "Send button",
    "numeric_key": lambda n: f"number {n} button on numeric keypad",
    "keypad_confirm": "checkmark confirm button on numeric keypad",
    "confirm_button": "Confirm button",
    "close_button": "X close button in Counter modal header"
}
```

## Timeouts e Waits

```python
TIMEOUTS = {
    "app_load": 3,
    "club_load": 2,
    "modal_open": 2,
    "keyboard_appear": 1,
    "search_results": 1,
    "selection": 1,
    "confirmation": 2,
    "close": 1
}
```
