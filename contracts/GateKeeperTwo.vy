# @version ^0.3.7

interface InstanceInterface:
    def entrant() -> address: view
    def enter(_gateKey: bytes8) -> bool: nonpayable

key: public(bytes8)

@external
@payable
def __init__(instance: address):
    mask: uint256 = convert(
        convert(
            convert(
                max_value(uint64),
                bytes8
            ),
            bytes32
        ),
        uint256
    )

    sender: uint256 = convert(
        keccak256(
            slice(
                convert(self, bytes32),
                12,
                20
            )
        ),
        uint256
    )

    key256: uint256 = sender ^ mask

    key: bytes8 = convert(
        slice(
            convert(key256, bytes32),
            0,
            8
        ),
        bytes8
    )

    assert InstanceInterface(instance).enter(key), "call failed"
    assert InstanceInterface(instance).entrant() == msg.sender, "!entrant"
    self.key = key
