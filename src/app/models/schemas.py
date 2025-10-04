from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional


class WalletCreateRequest(BaseModel):
    owners: List[str] = Field(..., min_length=1)
    threshold: int = Field(..., ge=1)
    timelock_seconds: Optional[int] = Field(default=0, ge=0)


class WalletResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    wallet_id: str
    owners: List[str]
    threshold: int
    timelock_seconds: int
    paused: bool


class PauseRequest(BaseModel):
    wallet_id: str


class ReplaceOwnerRequest(BaseModel):
    wallet_id: str
    old_owner: str
    new_owner: str


class WalletIdRequest(BaseModel):
    wallet_id: str


class SubmitTxRequest(BaseModel):
    wallet_id: str
    creator: str
    payload: Dict[str, Any]


class ConfirmTxRequest(BaseModel):
    wallet_id: str
    tx_id: str
    owner: str


class ExecuteTxRequest(BaseModel):
    wallet_id: str
    tx_id: str


class TxResponse(BaseModel):
    tx_id: str
    creator: str
    payload: Dict[str, Any]
    submitted_at: float
    confirmations: List[str]
    executed: bool

