# 🐍 Sistema de Gestão Financeira - Python Flask

Sistema completo de gestão financeira desenvolvido em **Python puro** com Flask.

## ✨ Características

- 🐍 **100% Python** - Sem Node.js ou npm necessário
- 🚀 **Flask** - Framework web minimalista
- 💾 **SQLite** - Banco de dados embutido
- 📱 **Responsivo** - Funciona em mobile e desktop
- ☁️ **Deploy Vercel** - Hospedagem gratuita

## 🎯 Funcionalidades

- ✅ Login e registro de usuários
- ✅ Adicionar despesas com parcelas
- ✅ Definir receitas mensais
- ✅ Cálculos automáticos (saldo, percentual)
- ✅ Marcar despesas como pagas
- ✅ Excluir despesas
- ✅ Dashboard interativo

## 📦 Instalação

### 1. Instalar Python

👉 **Baixe em:** https://www.python.org/downloads/

- Escolha Python 3.10 ou superior
- **IMPORTANTE:** Marque "Add Python to PATH" durante a instalação
- Reinicie o computador após instalar

### 2. Instalar Dependências

Abra o PowerShell nesta pasta e execute:

```powershell
python -m pip install -r requirements.txt
```

### 3. Executar o Sistema

```powershell
python app.py
```

Acesse: **http://localhost:5000**

## 🚀 Como Usar

### Primeira vez:
1. Clique em "Criar conta"
2. Preencha nome, email e senha
3. Você será automaticamente logado

### Dashboard:
1. Clique em **"+ Definir Receita"** para adicionar seu salário
2. Clique em **"+ Nova Despesa"** para adicionar gastos
3. Veja o resumo automático no topo
4. Marque despesas como pagas clicando no status
5. Exclua despesas clicando em "Excluir"

## ☁️ Deploy na Vercel

### 1. Criar repositório no GitHub

```powershell
git init
git add .
git commit -m "Sistema financeiro Python"
```

Crie repositório no GitHub e faça push.

### 2. Deploy na Vercel

1. Acesse: https://vercel.com
2. Faça login com GitHub
3. Click "New Project"
4. Selecione seu repositório
5. Click "Deploy"

**Pronto!** Seu sistema estará online!

## 🗄️ Banco de Dados

O sistema usa **SQLite** (arquivo `financeiro.db`):
- Criado automaticamente na primeira execução
- Não precisa configurar nada
- Todos os dados ficam salvos localmente

## 📂 Estrutura

```
C:\PGMD\Financeiro\
├── app.py                  # Aplicação Flask principal
├── requirements.txt        # Dependências Python
├── vercel.json            # Configuração Vercel
├── templates/             # Templates HTML
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
└── financeiro.db          # Banco de dados (criado automaticamente)
```

## 🔧 Tecnologias

- **Python 3.10+** - Linguagem
- **Flask 3.0** - Framework web
- **SQLite** - Banco de dados
- **HTML/CSS** - Interface
- **Jinja2** - Templates

## 🆘 Problemas Comuns

### "python não é reconhecido"
→ Instale o Python e marque "Add to PATH"

### "ModuleNotFoundError: No module named 'flask'"
→ Execute: `python -m pip install -r requirements.txt`

### Página em branco
→ Verifique se o servidor está rodando

### Não consigo criar conta
→ Verifique se o arquivo `financeiro.db` tem permissões de escrita

## 💡 Vantagens desta versão

✅ **Sem Node.js** - Só precisa de Python  
✅ **Sem npm** - Usa pip (gerenciador Python)  
✅ **Mais simples** - Menos dependências  
✅ **Rápido** - Leve e eficiente  
✅ **Deploy fácil** - Vercel suporta Python  

## 🎓 Para Desenvolvedores

### Adicionar nova rota:
```python
@app.route('/nova_rota')
@login_required
def nova_rota():
    return render_template('nova.html')
```

### Consultar banco de dados:
```python
conn = sqlite3.connect('financeiro.db')
c = conn.cursor()
c.execute('SELECT * FROM expenses')
dados = c.fetchall()
conn.close()
```

### Adicionar CSS personalizado:
Edite o `<style>` em `templates/base.html`

---

**Desenvolvido com 🐍 Python + ❤️**
