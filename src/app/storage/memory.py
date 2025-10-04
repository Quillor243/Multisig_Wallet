from typing import Dict
from src.app.core.types import Wallet, WalletId


class InMemoryStorage:
    def __init__(self) -> None:
        self.wallets: Dict[WalletId, Wallet] = {}

    def put_wallet(self, wallet: Wallet) -> None:
        self.wallets[wallet.wallet_id] = wallet

    def get_wallet(self, wallet_id: WalletId) -> Wallet:
        return self.wallets[wallet_id]

    def has_wallet(self, wallet_id: WalletId) -> bool:
        return wallet_id in self.wallets


storage = InMemoryStorage()

