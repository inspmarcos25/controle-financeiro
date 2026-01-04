# Instruções para enviar ao GitHub

## 1. Configure o Git (substitua com seus dados)
```bash
git config --global user.name "Seu Nome Completo"
git config --global user.email "seu.email@github.com"
```

## 2. Inicialize o repositório local
```bash
git init
git add .
git commit -m "Initial commit: Sistema de Controle Financeiro"
```

## 3. Crie um repositório no GitHub
1. Acesse https://github.com/new
2. Nome do repositório: `controle-financeiro` (ou outro nome)
3. Descrição: "Sistema de controle financeiro com Flask e SQLite"
4. Deixe **PÚBLICO** ou **PRIVADO** (sua escolha)
5. **NÃO** marque "Add README" (já temos)
6. Clique em "Create repository"

## 4. Conecte ao GitHub e faça o push
```bash
# Substitua SEU_USUARIO pelo seu username do GitHub
git remote add origin https://github.com/SEU_USUARIO/controle-financeiro.git
git branch -M main
git push -u origin main
```

## 5. Pronto!
Seu projeto estará no GitHub em:
`https://github.com/SEU_USUARIO/controle-financeiro`

---

## Comandos futuros úteis

### Fazer novos commits
```bash
git add .
git commit -m "Descrição da mudança"
git push
```

### Ver status
```bash
git status
```

### Ver histórico
```bash
git log --oneline
```
