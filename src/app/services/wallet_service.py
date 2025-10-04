import uuid
from typing import Dict, Any, List
from src.app.core.types import Wallet, Transaction
from src.app.core.errors import (
    WalletNotFoundError,
    NotAnOwnerError,
    AlreadyConfirmedError,
    ThresholdNotMetError,
    WalletPausedError,
    TimelockNotElapsedError,
    InvalidOperationError,
)
from src.app.storage.memory import storage
from src.app.core.security import current_timestamp


class WalletService:
    def create_wallet(self, owners: List[str], threshold: int, timelock_seconds: int) -> Dict[str, Any]:
        unique_owners = set(owners)
        if threshold > len(unique_owners):
            raise InvalidOperationError("threshold cannot exceed number of owners")
        wallet_id = str(uuid.uuid4())
        wallet = Wallet(
            wallet_id=wallet_id,
            owners=unique_owners,
            threshold=threshold,
            timelock_seconds=timelock_seconds,
        )
        storage.put_wallet(wallet)
        return {
            "wallet_id": wallet.wallet_id,
            "owners": sorted(wallet.owners),
            "threshold": wallet.threshold,
            "timelock_seconds": wallet.timelock_seconds,
            "paused": wallet.paused,
        }

    def _get_wallet(self, wallet_id: str) -> Wallet:
        if not storage.has_wallet(wallet_id):
            raise WalletNotFoundError("wallet not found")
        return storage.get_wallet(wallet_id)

    def pause(self, wallet_id: str) -> None:
        wallet = self._get_wallet(wallet_id)
        wallet.paused = True

    def unpause(self, wallet_id: str) -> None:
        wallet = self._get_wallet(wallet_id)
        wallet.paused = False

    def replace_owner(self, wallet_id: str, old_owner: str, new_owner: str) -> None:
        wallet = self._get_wallet(wallet_id)
        if old_owner not in wallet.owners:
            raise NotAnOwnerError("old owner is not in wallet")
        wallet.owners.remove(old_owner)
        wallet.owners.add(new_owner)

    def get_owners(self, wallet_id: str) -> List[str]:
        wallet = self._get_wallet(wallet_id)
        return sorted(wallet.owners)

    def submit_transaction(self, wallet_id: str, creator: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        wallet = self._get_wallet(wallet_id)
        if creator not in wallet.owners:
            raise NotAnOwnerError("creator is not an owner")
        tx_id = str(uuid.uuid4())
        tx = Transaction(
            tx_id=tx_id,
            creator=creator,
            payload=payload,
            submitted_at=current_timestamp(),
        )
        tx.confirmations.add(creator)  # авто-подтверждение инициатора по желанию
        wallet.transactions[tx_id] = tx
        return self._tx_to_dict(tx)

    def confirm_transaction(self, wallet_id: str, tx_id: str, owner: str) -> None:
        wallet = self._get_wallet(wallet_id)
        if owner not in wallet.owners:
            raise NotAnOwnerError("not an owner")
        if tx_id not in wallet.transactions:
            raise InvalidOperationError("transaction not found")
        tx = wallet.transactions[tx_id]
        if owner in tx.confirmations:
            raise AlreadyConfirmedError("already confirmed")
        if tx.executed:
            raise InvalidOperationError("already executed")
        tx.confirmations.add(owner)

    def execute_transaction(self, wallet_id: str, tx_id: str) -> Dict[str, Any]:
        wallet = self._get_wallet(wallet_id)
        if wallet.paused:
            raise WalletPausedError("wallet paused")
        if tx_id not in wallet.transactions:
            raise InvalidOperationError("transaction not found")
        tx = wallet.transactions[tx_id]
        if tx.executed:
            raise InvalidOperationError("already executed")
        if len(tx.confirmations) < wallet.threshold:
            raise ThresholdNotMetError("confirmations below threshold")
        # timelock
        now = current_timestamp()
        if wallet.timelock_seconds > 0 and now - tx.submitted_at < wallet.timelock_seconds:
            raise TimelockNotElapsedError("timelock not elapsed")
        tx.executed = True
        # Здесь можно интегрировать фактическое действие. Возвращаем payload как результат.
        return {"payload": tx.payload, "executed_at": now}

    def _tx_to_dict(self, tx: Transaction) -> Dict[str, Any]:
        return {
            "tx_id": tx.tx_id,
            "creator": tx.creator,
            "payload": tx.payload,
            "submitted_at": tx.submitted_at,
            "confirmations": sorted(list(tx.confirmations)),
            "executed": tx.executed,
        }


wallet_service = WalletService()

