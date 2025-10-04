from fastapi import FastAPI
from src.app.api.routes.health import router as health_router
from src.app.api.routes.wallet import router as wallet_router
from src.app.api.routes.transactions import router as tx_router
from src.app.api.routes.owners import router as owners_router


def create_app() -> FastAPI:
    app = FastAPI(title="Multisig Wallet API", version="0.1.0")
    app.include_router(health_router, prefix="/health", tags=["health"])
    app.include_router(wallet_router, prefix="/wallet", tags=["wallet"])
    app.include_router(tx_router, prefix="/tx", tags=["transactions"])
    app.include_router(owners_router, prefix="/owners", tags=["owners"])
    return app


app = create_app()

