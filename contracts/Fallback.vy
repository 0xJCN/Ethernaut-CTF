# @version ^0.3.7

contributions: public(HashMap[address, uint256])
owner: public(address)

@external
@view
def getContribution() -> uint256:
    return empty(uint256)

@external
@nonpayable
def withdraw():
    pass

@external
@payable
def contribute():
    pass

@external
@payable
def __default__():
    pass
