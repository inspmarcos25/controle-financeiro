# Sistema de Controle Financeiro - Instruções para AI

## Arquitetura do Projeto

Este é um sistema Flask monolítico que gerencia receitas e despesas pessoais:

- **[app.py](app.py)**: Aplicação completa (DB init, rotas, templates rendering)
- **SQLite Database** (`finance.db`): Auto-criado no primeiro run com schema fixo
- **Templates**: Jinja2 em [templates/](templates/) - `index.html` (dashboard) e `add_transaction.html` (form)
- **Frontend**: Vanilla JS + Chart.js para visualização, sem build step

### Fluxo de Dados Chave
1. DB inicializado ao importar `app.py` via `init_db()` - cria categorias padrão em português
2. Dashboard (`/`): Agrega transações via SQLite queries, opcionalmente filtra por mês (`?month=YYYY-MM`)
3. Form (`/add`): POST cria transações, suporta recorrência (gera múltiplos registros no loop)
4. Chart API (`/api/chart_data`): JSON endpoint alimenta Chart.js pie chart no dashboard

## Convenções do Projeto

### Database Patterns
- Use `sqlite3.Row` factory para dict-like access: `row['name']` ao invés de índices
- Sempre use context manager implícito: `conn = get_db(); conn.execute(...); conn.close()`
- Schema possui 2 tabelas: `categories` (pre-populated) e `transactions` (com FK)
- Transações têm type='income' ou type='expense' - nunca adicionar tipos novos sem migração

### Form Handling
- Recorrência implementada como loop inserindo múltiplas transações com datas calculadas:
  - Monthly = +30 dias aproximado (não date arithmetic preciso)
  - Ver [app.py:75-88](app.py#L75-L88) para lógica de repetições
- Categorias fixas no seed - adicionar novas requer execute manual no DB

### Frontend Integration
- Chart.js carregado via CDN (`<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>`)
- Fetch API em [index.html](templates/index.html) busca `/api/chart_data` e renderiza pie chart client-side
- Month picker usa query param `?month=YYYY-MM` - recarrega página inteira (não SPA)

## Workflows de Desenvolvimento

### Executar Local
```bash
python app.py  # Inicia em debug mode na porta 5000
```
Ou usar VS Code task "Run Flask App" (background task configurado)

### Database Debugging
- Use queries em [query.sql](query.sql) como referência - contém 15 queries úteis
- Inspecionar DB: `sqlite3 finance.db` então `.schema` ou queries do arquivo
- Reset completo: delete `finance.db` e restart app (auto-recria)

### Modificar Schema
- Não há migrations - alterar [app.py:13-31](app.py#L13-L31) `init_db()` e deletar DB
- Categorias padrão: sempre em português (Alimentação, Transporte, Salário, etc)

## Integração & Dependências

- **Única dependência**: Flask (ver [requirements.txt](requirements.txt))
- **No frontend build**: CSS/JS servidos estaticamente, sem webpack/vite
- **Chart.js**: Única lib externa, CDN-loaded, usado apenas em dashboard pie chart
- **Python stdlib**: `datetime` para date math, `sqlite3` para DB - sem ORMs

## Cuidados Específicos

- Date filtering usa `strftime('%Y-%m', date)` - requer formato YYYY-MM-DD nas inserções
- Amount sempre `REAL` no DB - converter string form inputs com `float()`
- Recurrent transactions não persistem metadata de recorrência - apenas geram N transações independentes
- Debug mode ativo no `app.run()` - desabilitar para produção