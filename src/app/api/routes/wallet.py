from fastapi import APIRouter, HTTPException
from src.app.services.wallet_service import wallet_service
from src.app.models.schemas import WalletCreateRequest, WalletResponse, PauseRequest, ReplaceOwnerRequest
from src.app.core.errors import MultisigError


router = APIRouter()


@router.post("/create", response_model=WalletResponse)
def create_wallet(body: WalletCreateRequest) -> WalletResponse:
    try:
        wallet = wallet_service.create_wallet(
            owners=body.owners,
            threshold=body.threshold,
            timelock_seconds=body.timelock_seconds or 0,
        )
        return WalletResponse(**wallet)
    except MultisigError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/pause")
def pause_wallet(body: PauseRequest) -> dict:
    try:
        wallet_service.pause(body.wallet_id)
        return {"status": "paused"}
    except MultisigError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/unpause")
def unpause_wallet(body: PauseRequest) -> dict:
    try:
        wallet_service.unpause(body.wallet_id)
        return {"status": "unpaused"}
    except MultisigError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/replace-owner")
def replace_owner(body: ReplaceOwnerRequest) -> dict:
    try:
        wallet_service.replace_owner(body.wallet_id, body.old_owner, body.new_owner)
        return {"status": "owner_replaced"}
    except MultisigError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

