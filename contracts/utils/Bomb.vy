# @version ^0.3.7

owner: immutable(address)

@external
@payable
def __init__():
    owner = msg.sender

@external
@payable
def __default__():
    assert tx.origin == owner, "!owner"
    addr: address = convert(slice(msg.data, 0, 32), address)
    selfdestruct(addr)
