# ☁️ Deploy na Vercel com Python

## 📋 Guia Completo de Deploy

### ✅ Pré-requisitos
- Conta no GitHub (grátis)
- Conta na Vercel (grátis)

---

## 🚀 Passo a Passo

### 1️⃣ Preparar o Repositório Git

Abra o PowerShell nesta pasta e execute:

```powershell
# Inicializar Git
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Sistema de gestão financeira em Python"
```

### 2️⃣ Criar Repositório no GitHub

1. Acesse: https://github.com
2. Clique em **"New repository"** (ou ícone +)
3. Nome: `gestao-financeira` (ou o que preferir)
4. Deixe **público** ou **privado** (ambos funcionam)
5. **NÃO** marque "Initialize with README"
6. Clique em **"Create repository"**

### 3️⃣ Conectar e Enviar para GitHub

No PowerShell, execute (substitua com sua URL):

```powershell
# Adicionar origem remota
git remote add origin https://github.com/SEU-USUARIO/gestao-financeira.git

# Renomear branch para main (se necessário)
git branch -M main

# Enviar para GitHub
git push -u origin main
```

**Dica:** Copie os comandos que aparecem na tela do GitHub!

### 4️⃣ Deploy na Vercel

1. Acesse: https://vercel.com
2. Clique em **"Sign Up"** ou **"Login"**
3. Escolha **"Continue with GitHub"**
4. Autorize a Vercel
5. Clique em **"New Project"**
6. Encontre seu repositório `gestao-financeira`
7. Clique em **"Import"**
8. **NÃO mude nada!** A Vercel detecta Python automaticamente
9. Clique em **"Deploy"**

### 5️⃣ Aguardar Deploy

- Vercel vai fazer o build (1-2 minutos)
- Quando aparecer **"Congratulations"**, está pronto!
- Clique em **"Visit"** para ver seu site online

---

## 🌐 Acessar Online

Sua aplicação estará em:
```
https://gestao-financeira-seu-usuario.vercel.app
```

Você pode compartilhar este link e acessar de qualquer lugar!

---

## 📱 Usar no Celular

1. Abra o navegador do celular
2. Digite a URL do seu site
3. Use normalmente!

💡 **Dica:** Adicione à tela inicial para usar como app!

---

## 🔄 Atualizar o Site

Quando fizer mudanças no código:

```powershell
# Adicionar mudanças
git add .

# Fazer commit
git commit -m "Descrição da mudança"

# Enviar para GitHub
git push
```

**A Vercel atualiza automaticamente!** ✨

---

## ⚠️ IMPORTANTE: Banco de Dados

O SQLite **NÃO persiste** na Vercel (ambiente serverless).

### Soluções:

**Opção 1: Para uso pessoal (local)**
- Use localmente: `python app.py`
- Dados salvos no arquivo `financeiro.db`

**Opção 2: Para produção (online)**
- Migre para PostgreSQL (Supabase, Railway, Neon)
- Requer mudanças no código

### Para usar SQLite online (temporário):

O banco será reiniciado a cada deploy. Use apenas para testes.

---

## 🔧 Configurações Avançadas

### Variáveis de Ambiente (se precisar):

1. No dashboard da Vercel
2. Vá em **Settings** → **Environment Variables**
3. Adicione suas variáveis
4. Clique em **Save**

### Domínio Customizado:

1. No dashboard da Vercel
2. Vá em **Settings** → **Domains**
3. Adicione seu domínio
4. Configure DNS

---

## 🆘 Problemas Comuns

### "Build failed"
✅ Verifique se `requirements.txt` está correto
✅ Certifique-se que `vercel.json` existe

### "Application Error"
✅ Veja os logs na Vercel
✅ Verifique se `app.py` está correto

### Banco de dados vazio após deploy
✅ Normal! SQLite não persiste na Vercel
✅ Use solução de banco online (Supabase, etc)

### Não consegue fazer push
✅ Verifique suas credenciais do GitHub
✅ Use `git config --global user.name "Seu Nome"`
✅ Use `git config --global user.email "seu@email.com"`

---

## 💡 Alternativas de Deploy

Se a Vercel não funcionar, tente:

### **PythonAnywhere** (recomendado para SQLite)
- https://www.pythonanywhere.com
- Grátis
- SQLite funciona perfeitamente
- Tutorial: https://help.pythonanywhere.com/pages/Flask/

### **Railway**
- https://railway.app
- Grátis com limites
- Suporta SQLite e PostgreSQL

### **Render**
- https://render.com
- Grátis
- Suporta Python + PostgreSQL

---

## 📊 Monitoramento

Na Vercel você pode ver:
- ✅ Número de acessos
- ✅ Tempo de resposta
- ✅ Logs de erro
- ✅ Analytics

---

## 🎉 Pronto!

Seu sistema está online e acessível de qualquer lugar do mundo!

**Compartilhe o link e use de onde estiver! 🌍**

---

**Deploy realizado com sucesso! ☁️✨**
