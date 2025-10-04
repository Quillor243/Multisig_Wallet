$ErrorActionPreference = "Stop"
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:8000/wallet/create -ContentType 'application/json' -Body '{"owners":["alice","bob","carol"],"threshold":2,"timelock_seconds":2}'

