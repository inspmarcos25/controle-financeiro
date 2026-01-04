import sqlite3

conn = sqlite3.connect('finance.db')
conn.row_factory = sqlite3.Row

print("=" * 50)
print("ESTRUTURA DO BANCO DE DADOS")
print("=" * 50)

tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print(f"\nTabelas encontradas: {[t['name'] for t in tables]}\n")

print("=" * 50)
print("CATEGORIAS")
print("=" * 50)
categories = conn.execute('SELECT * FROM categories').fetchall()
for cat in categories:
    print(f"ID: {cat['id']:2d} | Nome: {cat['name']}")

print("\n" + "=" * 50)
print("TRANSAÇÕES")
print("=" * 50)
transactions = conn.execute('''
    SELECT t.id, t.type, t.amount, c.name as category, t.date, t.description
    FROM transactions t
    LEFT JOIN categories c ON t.category_id = c.id
    ORDER BY t.date DESC
''').fetchall()

if len(transactions) == 0:
    print("\nNenhuma transação encontrada. O banco está vazio.")
else:
    print(f"\nTotal de transações: {len(transactions)}\n")
    for trans in transactions:
        tipo = "RECEITA" if trans['type'] == 'income' else "DESPESA"
        print(f"ID: {trans['id']:3d} | {tipo:8s} | R$ {trans['amount']:8.2f} | {trans['category']:15s} | {trans['date']} | {trans['description']}")

print("\n" + "=" * 50)
print("RESUMO FINANCEIRO")
print("=" * 50)
summary = conn.execute('''
    SELECT 
        SUM(CASE WHEN type='income' THEN amount ELSE 0 END) as total_income,
        SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) as total_expense
    FROM transactions
''').fetchone()

income = summary['total_income'] or 0
expense = summary['total_expense'] or 0
balance = income - expense

print(f"Total de Receitas:  R$ {income:10.2f}")
print(f"Total de Despesas:  R$ {expense:10.2f}")
print(f"Saldo:              R$ {balance:10.2f}")
print("=" * 50)

conn.close()
