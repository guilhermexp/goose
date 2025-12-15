# Automação PPPoker - Documentação Completa

## 📋 Visão Geral

Este projeto documenta o fluxo completo de automação para transferência de fichas no aplicativo PPPoker através do emulador Android. A automação foi mapeada, testada e documentada para uso por outros agentes de automação.

## ✅ Execução Realizada

**Data**: 11 de dezembro de 2025  
**Clube**: C.P.C. OnLine 2 (ID: 3330646)  
**Agente**: Varela.teste (ID: 13180661)  
**Valor Transferido**: 100 fichas  
**Status**: ✓ Sucesso  
**Tempo Total**: ~15 segundos

### Validação de Sucesso
- ✓ Saldo inicial: 68,487.75 → Saldo final: 68,387.75
- ✓ Saldo agente inicial: 422 → Saldo agente final: 522
- ✓ Mensagem "Success!" exibida
- ✓ Modal fechado corretamente

## 📁 Arquivos Gerados

### 1. **PPPoker_Automation_Script.md**
Documentação completa do fluxo com:
- Descrição detalhada de cada passo
- Elementos UI identificados
- Tempos de espera recomendados
- Validações necessárias
- Tratamento de erros
- Exemplo de execução completa

### 2. **PPPoker_Workflow_Template.md**
Template programático para implementação:
- Estrutura de código Python
- Seletores de elementos
- Classe PPPokerTransfer
- Configurações de timeout
- Métodos reutilizáveis

### 3. **PPPoker_Screenshots_Documentation.md**
Documentação visual detalhada:
- 13 screenshots documentados
- Descrição de elementos visíveis em cada tela
- Validações visuais
- Tabela resumo de estados
- Elementos críticos para automação

## 🔄 Fluxo de Automação (Resumo)

```
1. Abrir PPPoker
   ↓
2. Entrar no Clube "C.P.C. OnLine 2"
   ↓
3. Clicar em "Counter" (menu inferior)
   ↓
4. Buscar agente (Search Member)
   ↓
5. Digitar ID do agente (13180661)
   ↓
6. Selecionar agente nos resultados
   ↓
7. Clicar em "Send" e digitar valor (100)
   ↓
8. Confirmar transação
   ↓
9. Fechar modal do Counter
   ↓
✓ Sucesso!
```

## 🎯 Uso para Outros Agentes

### Opção 1: Seguir o Script Detalhado
Consulte `PPPoker_Automation_Script.md` para instruções passo a passo com todos os detalhes de implementação.

### Opção 2: Usar o Template Programático
Utilize `PPPoker_Workflow_Template.md` para implementar a automação em Python ou outra linguagem.

### Opção 3: Referência Visual
Use `PPPoker_Screenshots_Documentation.md` para entender os estados visuais e validações necessárias.

## 🔧 Parâmetros Configuráveis

```python
# Configurações básicas
CLUB_NAME = "C.P.C. OnLine 2"
AGENT_ID = "13180661"
TRANSFER_AMOUNT = 100

# Timeouts (segundos)
WAIT_APP_LOAD = 3
WAIT_CLUB_LOAD = 2
WAIT_MODAL_LOAD = 2
WAIT_KEYBOARD = 1
WAIT_CONFIRMATION = 2
```

## ⚠️ Pontos Críticos

1. **Validação de Saldo**: Sempre verificar saldo suficiente antes de iniciar
2. **IDs Únicos**: Cada agente tem um ID de 8 dígitos
3. **Confirmação Visual**: Aguardar mensagem "Success!" antes de considerar completo
4. **Atualização de Saldos**: Verificar que ambos os saldos foram atualizados
5. **Teclado Numérico**: Usar o teclado do app, não o do sistema

## 🛠️ Elementos UI Principais

### Seletores
- **App Icon**: "PPPoker app icon"
- **Club Card**: "Club card with name 'C.P.C. OnLine 2'"
- **Counter Icon**: "Counter icon in bottom navigation menu, third icon from left"
- **Search Field**: "Search Member text input field"
- **Send Button**: "Send button"
- **Confirm Button**: "Confirm button"

### Validações
- **Success Badge**: Badge verde com texto "Success!"
- **Balance Update**: Saldo diminui pelo valor transferido
- **Agent Balance**: Saldo do agente aumenta pelo valor transferido

## 📊 Estrutura de Dados Recomendada

```python
class PPPokerTransfer:
    club_name: str
    agent_id: str (8 dígitos)
    amount: int
    initial_balance: float
    final_balance: float
    agent_initial_balance: int
    agent_final_balance: int
    success: bool
```

## 🔍 Tratamento de Erros

| Erro | Solução |
|------|---------|
| App não abre | Verificar emulador e instalação |
| Clube não encontrado | Verificar login e acesso |
| Agente não encontrado | Verificar ID e clube correto |
| Saldo insuficiente | Verificar saldo antes de iniciar |
| Teclado não aparece | Clicar novamente no campo |

## 📈 Métricas de Execução

- **Passos Totais**: 11 ações principais
- **Tempo Médio**: 15 segundos
- **Taxa de Sucesso**: 100% (1/1 execuções)
- **Validações**: 13 pontos de verificação

## 🚀 Próximos Passos Sugeridos

1. **Implementar em código**: Usar o template para criar script executável
2. **Testes em lote**: Testar com múltiplas transferências
3. **Tratamento de exceções**: Adicionar try/catch para erros
4. **Logging**: Implementar sistema de logs detalhado
5. **Validações adicionais**: Adicionar verificações de segurança

## 📝 Notas Importantes

- Este fluxo foi testado e validado em 11/12/2025
- Versão do PPPoker: 4.2.56 (web)
- Emulador: Android (Pixel_7_API_34:5554)
- Todos os passos foram executados com sucesso
- Documentação completa e pronta para uso

## 📞 Suporte

Para dúvidas ou problemas na implementação:
1. Consulte primeiro o `PPPoker_Automation_Script.md`
2. Verifique os screenshots em `PPPoker_Screenshots_Documentation.md`
3. Use o template em `PPPoker_Workflow_Template.md` como referência

---

**Status do Projeto**: ✅ Completo e Validado  
**Última Atualização**: 11 de dezembro de 2025  
**Versão**: 1.0
