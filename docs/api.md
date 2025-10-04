# API

Базовый URL: `/`

- GET `/health/` → `{ status: "ok" }`
- POST `/wallet/create` → Body: `{ owners: string[], threshold: number, timelock_seconds?: number }`
  - 200: `WalletResponse`
- POST `/wallet/pause` → Body: `{ wallet_id: string }`
- POST `/wallet/unpause` → Body: `{ wallet_id: string }`
- POST `/wallet/replace-owner` → Body: `{ wallet_id: string, old_owner: string, new_owner: string }`
- POST `/owners/list` → Body: `{ wallet_id: string }` → `{ owners: string[] }`
- POST `/tx/submit` → Body: `{ wallet_id: string, creator: string, payload: object }` → `TxResponse`
- POST `/tx/confirm` → Body: `{ wallet_id: string, tx_id: string, owner: string }`
- POST `/tx/execute` → Body: `{ wallet_id: string, tx_id: string }` → `{ status, result }`

См. Swagger UI: `/docs`.
