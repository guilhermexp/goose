# Script de Automação PPPoker - Transferência de Fichas

## Descrição
Este script documenta o fluxo completo para realizar transferências de fichas no PPPoker através do emulador Android.

## Pré-requisitos
- Emulador Android em execução
- PPPoker instalado
- Acesso ao clube "C.P.C. OnLine 2"
- Saldo suficiente para transferência

## Fluxo de Automação

### Passo 1: Abrir PPPoker
**Ação:** Clicar no ícone do aplicativo PPPoker na tela inicial do Android
**Elemento:** Ícone do app PPPoker
**Tempo de espera:** 3 segundos (aguardar carregamento do app)
**Validação:** Tela de carregamento com versão do app (ex: Version-4.2.56 web)

### Passo 2: Entrar no Clube
**Ação:** Clicar no card do clube "C.P.C. OnLine 2"
**Elemento:** Card do clube com nome "C.P.C. OnLine 2" e contador de membros (ex: 2722)
**Tempo de espera:** 2 segundos
**Validação:** Tela do clube carregada com abas (TONGITS, TEEN PATTI, AOF, SNG, PLO H/L)

### Passo 3: Acessar Counter
**Ação:** Clicar no ícone "Counter" no menu inferior
**Elemento:** Terceiro ícone da esquerda para direita no menu de navegação inferior
**Tempo de espera:** 2 segundos
**Validação:** Modal "Counter" aberto com abas Trade, Send Items, Ticket

### Passo 4: Buscar Agente
**Ação:** Clicar no campo "Search Member"
**Elemento:** Campo de busca com placeholder "Search Member"
**Tempo de espera:** 1 segundo
**Validação:** Teclado Android aparece e campo está focado

### Passo 5: Digitar ID do Agente
**Ação:** Digitar o ID do agente (ex: 13180661)
**Método alternativo:** Clicar na sugestão do teclado se o ID aparecer
**Elemento:** Campo de texto ou botão de sugestão no teclado
**Tempo de espera:** 1 segundo
**Validação:** ID aparece no campo de busca e resultado é exibido

### Passo 6: Selecionar Agente
**Ação:** Clicar no resultado da busca
**Elemento:** Card do membro encontrado (ex: "Varela.teste" com ID e saldo)
**Tempo de espera:** 1 segundo
**Validação:** Checkmark verde aparece ao lado do agente selecionado

### Passo 7: Iniciar Envio
**Ação:** Clicar no botão "Send"
**Elemento:** Botão verde "Send" na parte inferior
**Tempo de espera:** 2 segundos
**Validação:** Modal "Send" abre com teclado numérico

### Passo 8: Digitar Valor
**Ação:** Digitar o valor a ser transferido usando o teclado numérico
**Sequência para 100:**
  1. Clicar no botão "1"
  2. Clicar no botão "0"
  3. Clicar no botão "0"
**Elemento:** Teclado numérico na parte inferior da tela
**Tempo de espera:** 1 segundo
**Validação:** Valor aparece no campo "Please enter the amount"

### Passo 9: Confirmar Valor
**Ação:** Clicar no botão de confirmação (checkmark) do teclado numérico
**Elemento:** Botão com ícone de checkmark (✓) no canto inferior direito do teclado
**Tempo de espera:** 2 segundos
**Validação:** Tela de confirmação aparece com "Total: [valor]" e botão "Confirm"

### Passo 10: Confirmar Transação
**Ação:** Revisar dados e clicar em "Confirm"
**Validação prévia:**
  - Verificar valor correto
  - Verificar agente correto
**Elemento:** Botão verde "Confirm"
**Tempo de espera:** 2 segundos
**Validação:** Mensagem "Success!" aparece e saldos são atualizados

### Passo 11: Fechar Modal
**Ação:** Clicar no botão X para fechar o modal Counter
**Elemento:** Botão "X" no canto superior direito do modal
**Tempo de espera:** 1 segundo
**Validação:** Retorno à tela principal do clube

## Variáveis do Script

```python
# Configurações
CLUB_NAME = "C.P.C. OnLine 2"
AGENT_ID = "13180661"  # ID do agente para transferência
TRANSFER_AMOUNT = 100  # Valor a ser transferido

# Tempos de espera (em segundos)
WAIT_APP_LOAD = 3
WAIT_CLUB_LOAD = 2
WAIT_MODAL_LOAD = 2
WAIT_KEYBOARD = 1
WAIT_SEARCH = 1
WAIT_CONFIRMATION = 2
```

## Elementos UI Identificados

### Tela Inicial Android
- **PPPoker Icon**: Ícone circular com logo do PPPoker

### Tela de Clubes
- **Club Card**: Card com nome do clube, ID e número de membros
- **Club Name**: "C.P.C. OnLine 2"

### Tela do Clube
- **Navigation Menu**: Menu inferior com 5 ícones
- **Counter Icon**: Terceiro ícone (ícone de fichas/moedas)

### Modal Counter
- **Tabs**: Trade, Send Items, Ticket
- **Search Field**: Campo "Search Member"
- **Member List**: Lista de membros com avatar, nome, ID e saldo
- **Send Button**: Botão verde "Send"
- **Reclaim Button**: Botão verde "Reclaim"

### Modal Send
- **Amount Field**: Campo "Please enter the amount"
- **Numeric Keypad**: Teclado com números 0-9 e botões especiais
- **Confirm Keypad Button**: Botão checkmark (✓)
- **Total Display**: "Total: [valor]"
- **Confirm Button**: Botão verde "Confirm"

### Indicadores de Sucesso
- **Success Message**: Badge verde com texto "Success!"
- **Balance Update**: Saldo atualizado no topo da tela
- **Agent Balance Update**: Saldo do agente atualizado na lista

## Tratamento de Erros

### Possíveis Erros e Soluções

1. **App não abre**
   - Verificar se emulador está rodando
   - Verificar se PPPoker está instalado
   - Tentar clicar novamente no ícone

2. **Clube não encontrado**
   - Verificar se está logado na conta correta
   - Verificar se tem acesso ao clube
   - Rolar a lista de clubes se necessário

3. **Agente não encontrado**
   - Verificar se o ID está correto
   - Verificar se o agente está no mesmo clube
   - Limpar campo de busca e tentar novamente

4. **Saldo insuficiente**
   - Verificar saldo disponível antes de iniciar
   - Ajustar valor da transferência

5. **Teclado não aparece**
   - Clicar novamente no campo
   - Aguardar mais tempo para carregamento

## Notas Importantes

1. **Validação de Saldo**: Sempre verificar se há saldo suficiente antes de iniciar a transferência
2. **Confirmação Visual**: Aguardar mensagem "Success!" antes de considerar transação concluída
3. **Atualização de Saldos**: Verificar que tanto o saldo próprio quanto o do agente foram atualizados
4. **IDs Únicos**: Cada agente tem um ID único de 8 dígitos
5. **Teclado Numérico**: Usar o teclado numérico do app, não o teclado do sistema

## Exemplo de Execução Completa

```
Início: Saldo = 68,487.75 | Agente (13180661) = 422
Transferência: 100 fichas
Fim: Saldo = 68,387.75 | Agente (13180661) = 522
Status: Success! ✓
```

## Logs de Execução

### Execução de Teste - 11/12/2025
- **Clube**: C.P.C. OnLine 2 (ID: 3330646)
- **Agente**: Varela.teste (ID: 13180661)
- **Valor**: 100 fichas
- **Saldo Inicial**: 68,487.75
- **Saldo Final**: 68,387.75
- **Saldo Agente Inicial**: 422
- **Saldo Agente Final**: 522
- **Status**: Sucesso
- **Tempo Total**: ~15 segundos
