# @version ^0.3.7

@external
@view
def token1() -> address:
    return empty(address)

@external
@view
def token2() -> address:
    return empty(address)

@external
@view
def balanceOf(token: address, account: address) -> uint256:
    return empty(uint256)

@external
def approve(spender: address, amount: uint256):
    pass

@external
def swap(_from: address, _to: address, amount: uint256):
    pass
