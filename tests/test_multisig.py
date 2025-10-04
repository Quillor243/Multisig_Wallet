from src.app.services.wallet_service import wallet_service


def test_submit_confirm_execute():
    # arrange
    w = wallet_service.create_wallet(["a", "b", "c"], threshold=2, timelock_seconds=0)
    wallet_id = w["wallet_id"]
    tx = wallet_service.submit_transaction(wallet_id, creator="a", payload={"op": "noop"})
    tx_id = tx["tx_id"]

    # act
    wallet_service.confirm_transaction(wallet_id, tx_id, owner="b")
    result = wallet_service.execute_transaction(wallet_id, tx_id)

    # assert
    assert result["payload"]["op"] == "noop"

