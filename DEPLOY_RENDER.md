# Deploy no Render.com

## Passo a Passo

### 1. Acesse o Render.com
- Vá para https://render.com
- Clique em **"Get Started"**
- Faça login com GitHub (ou crie uma conta)

### 2. Conecte seu repositório
- Clique em **"New +"** → **"Web Service"**
- Selecione **"Connect a repository"**
- Encontre `controle-financeiro`
- Clique em **"Connect"**

### 3. Configure o serviço
- **Name**: `controle-financeiro` (ou outro nome)
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Plan**: Free (gratuito)
- Clique em **"Create Web Service"**

### 4. Aguarde o deploy
- Render vai fazer o build automaticamente
- Pode levar 2-3 minutos
- Você receberá um URL como: `https://controle-financeiro.onrender.com`

### 5. Adicione seu domínio (opcional)
- Vá em **Settings** → **Custom Domains**
- Adicione seu domínio próprio
- Configure os DNS records conforme instruções

## Banco de Dados

⚠️ **Importante**: O banco de dados SQLite será **resetado** quando o Render reiniciar (grátis adormece após inatividade).

Para dados persistentes, considere:
- **PostgreSQL grátis no Render** (melhor opção)
- Migrar de SQLite para PostgreSQL
- Usar plano pago

## Comandos úteis

### Atualizar produção
Simplesmente faça `git push` - Render fará o deploy automaticamente!

```bash
git add .
git commit -m "Atualização"
git push
```

### Ver logs
Na dashboard do Render, abra **"Logs"** para debugar problemas.

## Problemas Comuns

### "Internal Server Error"
- Verifique os logs no Render
- Certifique-se que `gunicorn` está em requirements.txt

### Banco de dados vazio
- Normal no plano grátis (dados não persistem)
- Use PostgreSQL para dados permanentes

### Serviço não inicia
- Verifique se `app.py` tem `if __name__ == '__main__':`
- Confirme que **startCommand** é `gunicorn app:app`
