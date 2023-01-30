# @version ^0.3.7

from vyper.interfaces import ERC20

implements: ERC20

event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256

event Approval:
    owner: indexed(address)
    spender: indexed(address)
    value: uint256

totalSupply: public(uint256)

balanceOf: public(HashMap[address, uint256])
allowance: public(HashMap[address, HashMap[address, uint256]])

decimals: public(constant(uint8)) = 18

name: public(immutable(String[25]))
symbol: public(immutable(String[5]))

@external
@payable
def __init__(_name: String[25], _symbol: String[5], _supply: uint256, addr: address):
    init_supply: uint256 = _supply * 10 ** convert(decimals, uint256)
    self.balanceOf[msg.sender] = init_supply
    self.totalSupply = init_supply
    name = _name
    symbol = _symbol
     

@external
def approve(_spender: address, _value: uint256) -> bool:
    self.allowance[msg.sender][_spender] = _value
    log Approval(msg.sender, _spender, _value)
    return True

@external
def transferFrom(_from: address, _to: address, _value: uint256) -> bool:
    self.balanceOf[_from] -= _value
    self.balanceOf[_to] += _value
    self.allowance[_from][msg.sender] -= _value
    log Transfer(_from, _to, _value)
    return True

@external
def transfer(_to: address, _value: uint256) -> bool:
    self.balanceOf[msg.sender] -= _value
    self.balanceOf[_to] += _value
    log Transfer(msg.sender, _to, _value)
    return True
