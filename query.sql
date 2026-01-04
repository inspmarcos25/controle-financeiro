-- ============================================
-- CONSULTAS ÚTEIS - SISTEMA FINANCEIRO
-- ============================================

-- 1. VER TODAS AS CATEGORIAS
SELECT * FROM categories;

-- 2. VER TODAS AS TRANSAÇÕES
SELECT * FROM transactions;

-- 3. VER RECEITAS (INCOME)
SELECT * FROM transactions WHERE type = 'income' ORDER BY date DESC;

-- 4. VER DESPESAS (EXPENSE)
SELECT * FROM transactions WHERE type = 'expense' ORDER BY date DESC;

-- 5. TOTAL DE RECEITAS
SELECT SUM(amount) as total_receitas FROM transactions WHERE type = 'income';

-- 6. TOTAL DE DESPESAS
SELECT SUM(amount) as total_despesas FROM transactions WHERE type = 'expense';

-- 7. SALDO TOTAL (RECEITAS - DESPESAS)
SELECT 
  (SELECT SUM(amount) FROM transactions WHERE type = 'income') -
  (SELECT SUM(amount) FROM transactions WHERE type = 'expense') as saldo_total;

-- 8. DESPESAS POR CATEGORIA
SELECT c.name, SUM(t.amount) as total
FROM transactions t
JOIN categories c ON t.category_id = c.id
WHERE t.type = 'expense'
GROUP BY c.name
ORDER BY total DESC;

-- 9. RECEITAS POR CATEGORIA
SELECT c.name, SUM(t.amount) as total
FROM transactions t
JOIN categories c ON t.category_id = c.id
WHERE t.type = 'income'
GROUP BY c.name
ORDER BY total DESC;

-- 10. TRANSAÇÕES DO MÊS ATUAL
SELECT t.*, c.name as categoria
FROM transactions t
JOIN categories c ON t.category_id = c.id
WHERE strftime('%Y-%m', t.date) = strftime('%Y-%m', 'now')
ORDER BY t.date DESC;

-- 11. GASTOS POR DIA
SELECT date, type, SUM(amount) as total
FROM transactions
GROUP BY date, type
ORDER BY date DESC;

-- 12. TRANSAÇÕES ACIMA DE UM VALOR (ex: R$ 100)
SELECT t.*, c.name as categoria
FROM transactions t
JOIN categories c ON t.category_id = c.id
WHERE t.amount > 100
ORDER BY t.amount DESC;

-- 13. DESCRIÇÃO DE TODAS AS TRANSAÇÕES
SELECT 
  DATE(t.date) as data,
  t.type as tipo,
  c.name as categoria,
  t.amount as valor,
  t.description as descricao
FROM transactions t
JOIN categories c ON t.category_id = c.id
ORDER BY t.date DESC;

-- 14. CONTAR TRANSAÇÕES POR TIPO
SELECT type, COUNT(*) as quantidade
FROM transactions
GROUP BY type;

-- 15. GASTOS MENSAIS (ÚLTIMOS 12 MESES)
SELECT 
  strftime('%Y-%m', date) as mes,
  SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as receitas,
  SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as despesas
FROM transactions
GROUP BY mes
ORDER BY mes DESC;