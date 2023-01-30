# @version ^0.3.7

interface InstanceInterface:
    def setSolver(_solver: address): nonpayable

owner: immutable(address)

instance: InstanceInterface

@external
@payable
def __init__(_instance: InstanceInterface):
    owner = msg.sender
    self.instance = _instance
  
@external
def attack(solver: address):
    assert msg.sender == owner, "!owner"
    self.instance.setSolver(solver)
    # check our solver returns 42 before submitting
    res: Bytes[32] = raw_call(
        solver,
        method_id("whatIsTheMeaningOfLife()"),
        max_outsize=32,
    )
    assert convert(slice(res, 24, 8), uint8) == 42, "!42"
