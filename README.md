# Sistema de Controle Financeiro

Um sistema básico de controle financeiro desenvolvido em Python com Flask, permitindo gerenciar receitas, despesas, categorias e visualizar um dashboard.

## Funcionalidades

- Adicionar receitas e despesas
- Categorizar transações
- Dashboard com resumo financeiro e gráfico de despesas por categoria

## Como executar

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

2. Execute o aplicativo:
   ```
   python app.py
   ```

3. Abra o navegador em `http://127.0.0.1:5000/`

## Estrutura do Projeto

- `app.py`: Aplicação principal Flask
- `templates/`: Templates HTML
- `static/`: Arquivos CSS e JS
- `finance.db`: Banco de dados SQLite (criado automaticamente)