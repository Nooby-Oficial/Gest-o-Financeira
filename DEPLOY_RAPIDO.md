# 🚀 Deploy Rápido - GitHub + Vercel

## Passo 1: Enviar para o GitHub

```powershell
# Inicializar Git
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Sistema de gestão financeira completo"

# Criar repositório no GitHub (vá em github.com/new)
# Depois conecte e envie:
git remote add origin https://github.com/SEU_USUARIO/financeiro.git
git branch -M main
git push -u origin main
```

## Passo 2: Deploy na Vercel

1. Acesse: https://vercel.com
2. Clique em **"Add New Project"**
3. Clique em **"Import Git Repository"**
4. Selecione seu repositório `financeiro`
5. Clique em **"Deploy"**

**Pronto!** A Vercel detecta automaticamente que é Python e faz o deploy.

## ⚠️ IMPORTANTE: Limitação do SQLite

O SQLite **NÃO persiste dados** no Vercel (ambiente serverless). Para produção, você precisa usar um banco de dados externo:

### Opções Gratuitas:
- **Supabase** (PostgreSQL) - 500MB grátis
- **PlanetScale** (MySQL) - 5GB grátis
- **MongoDB Atlas** - 512MB grátis

## 🔄 Para usar PostgreSQL (Supabase):

1. Crie conta em https://supabase.com
2. Crie novo projeto
3. Copie a Connection String
4. Instale psycopg2: adicione em `requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   ```
5. Modifique `app.py` para usar PostgreSQL ao invés de SQLite

## 📱 Acesso Online

Após o deploy, você receberá uma URL tipo:
```
https://financeiro-abc123.vercel.app
```

Você poderá acessar de qualquer lugar do mundo! 🌎
