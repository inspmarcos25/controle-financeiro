# Configurar PostgreSQL no Render - Guia Completo

## Passo 1: Criar PostgreSQL Database no Render

1. Acesse https://dashboard.render.com
2. Clique em **"New +"** → **"PostgreSQL"**
3. Preencha:
   - **Name**: `controle-financeiro-db`
   - **Database**: `finance_db`
   - **User**: (deixe auto-gerado)
   - **Region**: Escolha o mais próximo (ex: Ohio ou Oregon)
   - **PostgreSQL Version**: 16
   - **Instance Type**: **Free** (0 GB, será deletado após 90 dias de inatividade)
4. Clique em **"Create Database"**
5. ⏳ Aguarde 2-3 minutos até status ficar **"Available"**

## Passo 2: Copiar URL do Banco

1. Na página do banco criado, procure por **"Internal Database URL"**
2. Copie a URL completa (formato: `postgres://usuario:senha@...`)
3. **GUARDE ESSA URL!** Você vai precisar dela no próximo passo

## Passo 3: Configurar Variável de Ambiente no Web Service

1. Volte para Dashboard → Clique no seu web service **"controle-financeiro"**
2. Vá em **"Environment"** (menu lateral esquerdo)
3. Clique em **"Add Environment Variable"**
4. Adicione:
   - **Key**: `DATABASE_URL`
   - **Value**: Cole a URL que você copiou no Passo 2
5. Clique em **"Save Changes"**

## Passo 4: Deploy Automático

O Render detectará a mudança e fará o deploy automaticamente.

Aguarde 3-5 minutos e acesse seu site!

---

## ✅ Pronto!

Agora seu projeto usa PostgreSQL no Render (dados persistem) e SQLite localmente (desenvolvimento).

### Como testar:

1. Adicione transações no site do Render
2. Faça um novo deploy (commit no GitHub)
3. Verifique se as transações **continuam lá** ✨

---

## Solução de Problemas

### "relation does not exist"
- O banco não foi inicializado. Reinicie o web service no Render.

### "psycopg2 not found"
- Commit o `requirements.txt` atualizado e faça push.

### Banco foi deletado após 90 dias
- Planos gratuitos do Render deletam bancos inativos. Use o banco semanalmente ou considere upgrade.
