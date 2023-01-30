# @version ^0.3.7

interface InstanceInterface:
    def cryptoVault() -> address: view
    def forta() -> address: view

interface IForta:
    def raiseAlert(user: address): nonpayable

interface IDetectionBot:
    def handleTransaction(user: address, msgData: Bytes[100]): nonpayable

implements: IDetectionBot

owner: immutable(address)

instance: InstanceInterface
vault: address

forta: public(IForta)

@external
@payable
def __init__(_instance: InstanceInterface):
    owner = msg.sender
    self.instance = _instance
    self.forta = IForta(self.instance.forta())
    self.vault = self.instance.cryptoVault()

@external
def handleTransaction(user: address, msgData: Bytes[100]):
    assert msg.sender == self.forta.address, "!forta"
    to: address = empty(address)
    value: uint256 = empty(uint256)
    sender: address = empty(address)
    to, value, sender = _abi_decode(
        slice(msgData, 4, 96),
        (address,uint256,address),
    )
    if sender == self.vault:
        self.forta.raiseAlert(user)
