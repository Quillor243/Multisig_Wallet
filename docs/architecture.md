# Архитектура

Сервис реализует мультисиг (M-of-N): для выполнения транзакции требуется не менее M подтверждений от владельцев из множества N.

Основные сущности:
- Wallet: owners, threshold M, timelock, paused, transactions
- Transaction: creator, payload, submitted_at, confirmations, executed

Потоки:
1) submit → создаёт транзакцию, фиксирует submitted_at, авто-подтверждение автора
2) confirm → добавляет подпись владельца, проверяет дубли
3) execute → проверяет paused, timelock, порог M, помечает executed

Замена владельца: remove(old_owner) + add(new_owner), без изменения threshold.
Защитная пауза: глобальная для кошелька, блокирует execute до unpause.

Хранилище: InMemory (можно заменить на БД через адаптер).
API: FastAPI, синхронные эндпоинты для простоты.
