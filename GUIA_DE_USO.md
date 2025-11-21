# 🎓 GUIA DE USO - Sistema de Gestão Financeira

## 📝 Primeira Vez - Criar Conta

1. Execute o sistema: `python app.py`
2. Acesse: http://localhost:5000
3. Clique em **"Criar conta"**
4. Preencha:
   - Nome completo
   - Email (será seu login)
   - Senha (mínimo 6 caracteres)
   - Confirme a senha
5. Clique em **"Criar conta"**

✅ Você será automaticamente redirecionado para o dashboard!

---

## 🔐 Login

Se já tem conta:
1. Digite seu email
2. Digite sua senha
3. Clique em **"Entrar"**

---

## 💰 Dashboard - Tela Principal

### Cards de Resumo (no topo):

**1. Receita** (verde)
- Total de todas as suas receitas

**2. Despesas** (vermelho)
- Soma de todas as parcelas mensais

**3. Saldo** (verde ou vermelho)
- Receita - Despesas
- Verde = sobrou dinheiro
- Vermelho = gastou mais que ganhou

**4. % Utilizado** (azul)
- Percentual da receita já comprometido
- Ex: 75% = você já gastou 75% do seu salário

---

## 💵 Adicionar Receita (Salário)

1. Clique em **"+ Definir Receita"**
2. Preencha:
   - **Descrição:** Ex: "Salário", "Freelance", "Renda Extra"
   - **Valor:** Quanto você recebe (ex: 3500.00)
   - **Mês/Ano:** Selecione o mês/ano
3. Clique em **"Salvar"**

💡 **Dica:** Você pode adicionar múltiplas receitas no mesmo mês!

---

## 💳 Adicionar Despesa

1. Clique em **"+ Nova Despesa"**
2. Preencha os campos:

### Descrição *
O que você está gastando
- Ex: "Conta de luz", "Supermercado", "Internet"

### Valor Total *
Quanto vai custar no total
- Ex: 150.00 (conta de luz)
- Ex: 1200.00 (celular parcelado)

### Parcelas *
Em quantas vezes vai dividir
- 1 = à vista
- 3 = dividir em 3 vezes
- 12 = dividir em 12 vezes

💡 **O sistema calcula automaticamente** o valor da parcela!

### Data de Vencimento *
Quando a conta vence
- Selecione no calendário

### Categoria (opcional)
Para organizar seus gastos
- Ex: "Moradia", "Alimentação", "Transporte", "Lazer"

3. Clique em **"Criar"**

---

## 📊 Tabela de Despesas

A tabela mostra todas as suas despesas com:

| Coluna | O que mostra |
|--------|-------------|
| **Descrição** | Nome da despesa |
| **Categoria** | Tipo do gasto |
| **Valor Total** | Quanto custa no total |
| **Parcelas** | Em quantas vezes dividiu |
| **Valor/Parcela** | Quanto paga por mês |
| **Vencimento** | Quando vence |
| **Status** | Pago ou Pendente |
| **Ações** | Botão para excluir |

---

## ✅ Marcar como Pago/Pendente

Na coluna "Status", você verá um badge:
- 🟡 **Pendente** = ainda não pagou
- 🟢 **Pago** = já pagou

**Para mudar:**
- Clique no badge
- Ele alternará entre Pendente ↔ Pago

---

## 🗑️ Excluir Despesa

1. Na tabela, encontre a despesa
2. Clique em **"Excluir"** (botão vermelho)
3. Confirme a exclusão
4. A despesa será removida permanentemente

---

## 💡 Exemplos Práticos

### Exemplo 1: Conta Mensal
```
Descrição: Conta de luz
Valor Total: 150.00
Parcelas: 1
Data: 10/12/2025
Categoria: Moradia
```
**Resultado:** Vai descontar R$ 150,00 do seu saldo

---

### Exemplo 2: Compra Parcelada
```
Descrição: Celular novo
Valor Total: 2400.00
Parcelas: 12
Data: 15/12/2025
Categoria: Tecnologia
```
**Resultado:** Vai descontar R$ 200,00 por mês (durante 12 meses)

---

### Exemplo 3: Múltiplas Receitas
```
Receita 1:
- Descrição: Salário
- Valor: 3500.00
- Mês: 11/2025

Receita 2:
- Descrição: Freelance
- Valor: 800.00
- Mês: 11/2025

Total de Receita: R$ 4.300,00
```

---

## 🔄 Fluxo de Uso Diário

### Início do Mês:
1. Defina sua receita mensal (salário)
2. Adicione as contas fixas (luz, água, internet)

### Durante o Mês:
1. Adicione despesas conforme surgem
2. Marque como "pago" quando pagar
3. Acompanhe seu saldo em tempo real

### Fim do Mês:
1. Revise seus gastos
2. Compare receita vs despesas
3. Veja onde pode economizar
4. Planeje o próximo mês

---

## 📱 Acesso Mobile

O sistema é **totalmente responsivo**:
- Funciona no celular
- Funciona no tablet
- Funciona no computador

Basta acessar pelo navegador!

---

## 🎯 Dicas de Uso

### ✅ Boas Práticas:

1. **Adicione despesas imediatamente**
   - Não deixe acumular

2. **Use categorias consistentes**
   - Facilita acompanhar onde gasta mais

3. **Marque como pago quando pagar**
   - Mantenha o controle atualizado

4. **Revise semanalmente**
   - Veja se está dentro do orçamento

5. **Planeje compras parceladas**
   - Verifique se o valor da parcela cabe no orçamento

---

## 🆘 Problemas Comuns

### "Nenhuma despesa cadastrada"
✅ Normal! Clique em "+ Nova Despesa" para começar

### "Total de receita: R$ 0,00"
✅ Clique em "+ Definir Receita" para adicionar seu salário

### Dashboard vazio
✅ Adicione receitas e despesas para ver os dados

### Não consigo excluir
✅ Verifique se está logado com o usuário correto

---

## 🎉 Pronto para Controlar suas Finanças!

Agora você tem todas as ferramentas para:
- ✅ Controlar gastos
- ✅ Acompanhar saldo
- ✅ Planejar compras
- ✅ Economizar dinheiro

**Boa gestão financeira! 💰📊**
