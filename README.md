# Multisig Wallet (M-of-N)

Многоуровневый проект мультисиг-кошелька (M-of-N) с поддержкой:

- submit / confirm / execute жизненного цикла транзакций
- замены владельца (owner replace)
- защитной паузы (pause/unpause) и timelock

REST API на FastAPI, внутреннее ядро, документация и инфраструктура (Docker, CI).

## Быстрый старт

```bash
python -m venv .venv
. .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.app.main:app --reload
```

Откройте `http://127.0.0.1:8000/docs` для Swagger UI.

## Структура проекта

```
src/
  app/
    main.py
    api/
      routes/
        health.py
        wallet.py
        transactions.py
        owners.py
    core/
      multisig.py (см. services/wallet_service.py)
      errors.py
      types.py
      security.py
    models/
      schemas.py
    services/
      wallet_service.py
    storage/
      memory.py
docs/
  architecture.md
  api.md
  SECURITY.md
infra/
  Dockerfile
  docker-compose.yml
.github/
  workflows/
    ci.yml
scripts/
  run_dev.ps1
  init_demo.ps1
tests/
  test_multisig.py
requirements.txt
README.md
```

Больше деталей в `docs/architecture.md` и `docs/api.md`.

## Лицензия

MIT

