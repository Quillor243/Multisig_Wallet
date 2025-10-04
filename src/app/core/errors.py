class MultisigError(Exception):
    pass


class WalletNotFoundError(MultisigError):
    pass


class TransactionNotFoundError(MultisigError):
    pass


class NotAnOwnerError(MultisigError):
    pass


class AlreadyConfirmedError(MultisigError):
    pass


class ThresholdNotMetError(MultisigError):
    pass


class WalletPausedError(MultisigError):
    pass


class TimelockNotElapsedError(MultisigError):
    pass


class InvalidOperationError(MultisigError):
    pass

