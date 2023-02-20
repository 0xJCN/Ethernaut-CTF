# @version ^0.3.7

# functions in proxy contract

@external
@view
def pendingAdmin() -> address:
    return empty(address)

@external
@view
def admin() -> address:
    return empty(address)

@external
def proposeNewAdmin(_newAdmin: address):
    pass

# functions in implementation contract

@external
@view
def owner() -> address:
    return empty(address)

@external
@view
def whitelisted(addr: address) -> bool:
    return empty(bool)

@external
@view
def balances(addr: address) -> uint256:
    return empty(uint256)

@external
@view
def maxBalance() -> uint256:
    return empty(uint256)


@external
def setMaxBalance(_maxBalance: uint256):
    pass

@external
def addToWhitelist(addr: address):
    pass

@external
@payable
def deposit():
    pass

@external
@payable
def execute(to: address, amount: uint256, data: Bytes[32]):
    pass

@external
@payable
def multicall(data: DynArray[Bytes[32], 32]):
    pass
