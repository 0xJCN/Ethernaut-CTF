# @version ^0.3.7

owner: immutable(address)

@external
@payable
def __init__():
    owner = msg.sender

event Print:
    data: indexed(address)

@external
@payable
def __default__():
    assert tx.origin == owner, "!owner"
    log Print(convert(slice(msg.data, 0, 32), address))
    addr: address = convert(slice(msg.data, 0, 32), address)
    selfdestruct(addr)
