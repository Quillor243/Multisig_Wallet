from fastapi import APIRouter, HTTPException
from src.app.services.wallet_service import wallet_service
from src.app.models.schemas import WalletIdRequest
from src.app.core.errors import MultisigError


router = APIRouter()


@router.post("/list")
def list_owners(body: WalletIdRequest) -> dict:
    try:
        owners = wallet_service.get_owners(body.wallet_id)
        return {"owners": owners}
    except MultisigError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

