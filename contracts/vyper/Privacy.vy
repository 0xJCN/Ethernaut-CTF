# @version ^0.3.7

interface InstanceInterface:
    def locked() -> bool: view
    def unlock(_key: bytes16): nonpayable

owner: immutable(address)

instance: InstanceInterface

@external
@payable
def __init__(_instance: InstanceInterface):
    owner = msg.sender
    self.instance = _instance
  
@external
def attack(key: bytes16):
    assert msg.sender == owner, "!owner"
    self.instance.unlock(key)
    assert self.instance.locked() == False, "!passed"
