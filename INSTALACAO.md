# 🚀 GUIA DE INSTALAÇÃO RÁPIDO

## ✅ Passo 1: Instalar Python

### Windows:
1. Acesse: **https://www.python.org/downloads/**
2. Baixe **Python 3.10+** (botão amarelo)
3. Execute o instalador
4. ⚠️ **IMPORTANTE:** Marque ☑️ "Add Python to PATH"
5. Clique em "Install Now"
6. Aguarde a instalação
7. **Reinicie o computador**

### Verificar instalação:
Abra o PowerShell e digite:
```powershell
python --version
```

Deve aparecer algo como: `Python 3.10.x`

---

## ✅ Passo 2: Instalar Dependências

Abra o PowerShell **nesta pasta** (`C:\PGMD\Financeiro`) e execute:

```powershell
python -m pip install -r requirements.txt
```

Aguarde a instalação (10-30 segundos).

---

## ✅ Passo 3: Executar o Sistema

No PowerShell, execute:

```powershell
python app.py
```

Você verá algo como:
```
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

---

## ✅ Passo 4: Acessar no Navegador

Abra o navegador e acesse:

**http://localhost:5000**

---

## 🎉 Pronto! Agora você pode:

1. **Criar sua conta** na tela de registro
2. **Fazer login**
3. **Adicionar receitas** (seu salário)
4. **Cadastrar despesas**
5. **Ver seu saldo em tempo real**

---

## 🌐 Deploy Online (Opcional)

### Para colocar na internet:

1. Crie conta no GitHub
2. Crie repositório
3. Faça push do código:
```powershell
git init
git add .
git commit -m "Sistema financeiro"
git remote add origin https://github.com/seu-usuario/seu-repo.git
git push -u origin main
```

4. Acesse https://vercel.com
5. Faça login com GitHub
6. Importe seu repositório
7. Click "Deploy"

**Pronto!** Seu sistema estará online e acessível de qualquer lugar!

---

## 🆘 Ajuda

### Python não é reconhecido?
1. Reinstale o Python
2. Marque "Add Python to PATH"
3. Reinicie o PC

### Erro ao instalar dependências?
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Porta 5000 em uso?
Edite `app.py` e mude:
```python
app.run(debug=True, host='0.0.0.0', port=8000)
```

---

**Sistema 100% funcional e pronto para uso! 🎉**
