from typing import List, Dict, Set, Any, Optional
from dataclasses import dataclass, field


TxId = str
WalletId = str


@dataclass
class Transaction:
    tx_id: TxId
    creator: str
    payload: Dict[str, Any]
    submitted_at: float
    confirmations: Set[str] = field(default_factory=set)
    executed: bool = False


@dataclass
class Wallet:
    wallet_id: WalletId
    owners: Set[str]
    threshold: int
    timelock_seconds: int = 0
    paused: bool = False
    transactions: Dict[TxId, Transaction] = field(default_factory=dict)

