# Documentação de Screenshots - Fluxo PPPoker

## Visão Geral
Este documento descreve os estados visuais de cada passo do fluxo de transferência de fichas no PPPoker.

---

## Screenshot 1: Tela Inicial Android
**Passo**: Início do fluxo
**Elementos Visíveis**:
- Ícone do PPPoker (circular com logo verde)
- Barra de status Android no topo
- Data e hora: "Thu, Dec 11"
- Barra de busca Google na parte inferior

**Ação**: Clicar no ícone do PPPoker

---

## Screenshot 2: Carregamento do PPPoker
**Passo**: App abrindo
**Elementos Visíveis**:
- Tela de splash com ilustração do prédio PPPoker
- Texto "Version-4.2.56 (web)" no topo
- Arte gráfica com edifícios e ambiente noturno

**Validação**: App está carregando corretamente

---

## Screenshot 3: Tela de Clubes
**Passo**: Seleção do clube
**Elementos Visíveis**:
- Header "CLUB" no topo
- Card do clube "C.P.C. OnLine 2"
  - Logo CPC
  - Nome do clube
  - Número de membros: 2722
  - Estrelas de classificação
- Mensagem "Long press to expand your list of Clubs"
- Menu inferior: SHOP, FORUM, (Home), CAREER, PROFILE

**Ação**: Clicar no card "C.P.C. OnLine 2"

---

## Screenshot 4: Tela do Clube
**Passo**: Dentro do clube
**Elementos Visíveis**:
- Header com nome "C.P.C. OnLine 2" e Club ID: 3330646
- Saldo exibido: 68,487.75
- Jackpot counter no canto superior direito
- Abas de jogos: TONGITS, TEEN PATTI, AOF, SNG, PLO H/L
- Filtros: Active, Open Seats
- Banner "Global Tournament"
- Área vazia com "No results found"
- Menu inferior com 5 ícones (Counter é o 3º)

**Ação**: Clicar no ícone Counter (3º ícone da esquerda)

---

## Screenshot 5: Modal Counter Aberto
**Passo**: Counter acessado
**Elementos Visíveis**:
- Título "Counter" no topo
- Botão X para fechar no canto superior direito
- Três abas: Trade (ativa), Send Items, Ticket
- Saldos exibidos: 68,487.75 (principal), 422, 2.13M
- Campo "Search Member" com ícone de lupa
- Filtros: Member: 0, Verified: 0, Time joined
- Botões na parte inferior: Send (verde), Reclaim (verde)

**Ação**: Clicar no campo "Search Member"

---

## Screenshot 6: Campo de Busca Ativo
**Passo**: Busca de agente
**Elementos Visíveis**:
- Campo "Search Member" focado
- Teclado Android QWERTY visível
- Sugestão "13180661" aparece no teclado
- Lista de membros visível
- Botão "OK" visível

**Ação**: Clicar na sugestão "13180661" ou digitar o ID

---

## Screenshot 7: Resultado da Busca
**Passo**: Agente encontrado
**Elementos Visíveis**:
- Campo de busca mostra "13180661"
- Resultado encontrado:
  - Nome: Varela.teste
  - ID: 13180661
  - Nickname: pp13180661
  - Saldo: 422 fichas
  - Ícone de verificação verde
- Teclado ainda visível

**Ação**: Clicar no resultado "Varela.teste"

---

## Screenshot 8: Agente Selecionado
**Passo**: Agente marcado para transferência
**Elementos Visíveis**:
- Varela.teste selecionado com checkmark verde ✓
- Saldo do agente: 422
- Teclado fechado
- Botões visíveis: Send (verde), Reclaim (verde)
- Campo de busca ainda mostra "13180661"

**Ação**: Clicar no botão "Send"

---

## Screenshot 9: Modal Send com Teclado Numérico
**Passo**: Inserção de valor
**Elementos Visíveis**:
- Título "Send" no topo
- Saldo disponível: 68,487.75
- Campo "Please enter the amount" com X para limpar
- Agente selecionado: Varela.teste (422 fichas) com checkmark
- Teclado numérico: Números 1-9, 0, botões especiais

**Ação**: Digitar "100" usando o teclado numérico

---

## Screenshot 10: Valor Digitado
**Passo**: Valor inserido
**Elementos Visíveis**:
- Campo mostra "100"
- Agente: Varela.teste (422) ainda selecionado
- Teclado numérico ainda visível

**Ação**: Clicar no botão checkmark ✓ do teclado

---

## Screenshot 11: Tela de Confirmação
**Passo**: Revisão antes de confirmar
**Elementos Visíveis**:
- Título "Send" mantido
- Campo mostra "100"
- Agente: Varela.teste (422)
- Teclado fechado
- **"Total: 100"** exibido na parte inferior
- Botão "Confirm" (verde) proeminente

**Validação Necessária**:
- Valor correto: 100 ✓
- Agente correto: Varela.teste (13180661) ✓

**Ação**: Clicar em "Confirm"

---

## Screenshot 12: Transferência Concluída
**Passo**: Sucesso da operação
**Elementos Visíveis**:
- Badge verde "Success!" no topo
- Saldo atualizado: 68,387.75 (diminuiu 100)
- Campo de busca mostra "13180661"
- Agente Varela.teste agora mostra: **522 fichas** (aumentou 100)
- Checkmark ainda visível no agente
- Botões Send e Reclaim disponíveis

**Validação de Sucesso**:
- Mensagem "Success!" ✓
- Saldo próprio: 68,487.75 → 68,387.75 ✓
- Saldo agente: 422 → 522 ✓

**Ação**: Clicar no X para fechar o modal

---

## Screenshot 13: Retorno à Tela do Clube
**Passo**: Fluxo concluído
**Elementos Visíveis**:
- Tela principal do clube "C.P.C. OnLine 2"
- Saldo atualizado visível: 68,387.75
- Todas as abas de jogos visíveis
- Menu inferior normal
- Modal Counter fechado

**Validação Final**: Transferência completada com sucesso

---

## Resumo de Estados Visuais

| Passo | Tela | Elemento Chave | Validação |
|-------|------|----------------|-------------|
| 1 | Android Home | Ícone PPPoker | Ícone visível |
| 2 | Splash Screen | Version text | App carregando |
| 3 | Lista de Clubes | Card CPC | Clube visível |
| 4 | Tela do Clube | Menu inferior | Dentro do clube |
| 5 | Modal Counter | Abas Trade/Send/Ticket | Counter aberto |
| 6 | Busca Ativa | Teclado QWERTY | Campo focado |
| 7 | Resultado | Varela.teste | Agente encontrado |
| 8 | Seleção | Checkmark verde | Agente selecionado |
| 9 | Modal Send | Teclado numérico | Pronto para digitar |
| 10 | Valor Inserido | "100" no campo | Valor correto |
| 11 | Confirmação | Total: 100 | Dados corretos |
| 12 | Sucesso | Success! badge | Transferência OK |
| 13 | Clube | Saldo atualizado | Fluxo completo |

---

## Elementos UI Críticos para Automação

### Identificação de Sucesso
1. **Badge "Success!"**: Cor verde, aparece no topo do modal
2. **Atualização de Saldo**: Valor diminui exatamente pelo montante transferido
3. **Saldo do Agente**: Aumenta exatamente pelo montante transferido

### Elementos de Navegação
1. **Botão X**: Sempre no canto superior direito dos modais
2. **Botões de Ação**: Sempre verdes, na parte inferior
3. **Checkmarks**: Verde para seleção, azul claro para confirmação

### Campos de Entrada
1. **Search Member**: Aceita texto e números
2. **Amount Field**: Apenas números via teclado numérico

### Indicadores de Estado
1. **Saldo no Topo**: Sempre visível, atualiza em tempo real
2. **Checkmark no Agente**: Indica seleção ativa
3. **Total Display**: Mostra valor antes da confirmação final
