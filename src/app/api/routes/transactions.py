from fastapi import APIRouter, HTTPException
from src.app.services.wallet_service import wallet_service
from src.app.models.schemas import (
    SubmitTxRequest,
    ConfirmTxRequest,
    ExecuteTxRequest,
    TxResponse,
)
from src.app.core.errors import MultisigError


router = APIRouter()


@router.post("/submit", response_model=TxResponse)
def submit_tx(body: SubmitTxRequest) -> TxResponse:
    try:
        tx = wallet_service.submit_transaction(
            wallet_id=body.wallet_id,
            creator=body.creator,
            payload=body.payload,
        )
        return TxResponse(**tx)
    except MultisigError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/confirm")
def confirm_tx(body: ConfirmTxRequest) -> dict:
    try:
        wallet_service.confirm_transaction(
            wallet_id=body.wallet_id, tx_id=body.tx_id, owner=body.owner
        )
        return {"status": "confirmed"}
    except MultisigError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/execute")
def execute_tx(body: ExecuteTxRequest) -> dict:
    try:
        result = wallet_service.execute_transaction(
            wallet_id=body.wallet_id, tx_id=body.tx_id
        )
        return {"status": "executed", "result": result}
    except MultisigError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

