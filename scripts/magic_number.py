from ape import accounts, project
from .utils.helper import get_level_instance, level_completed, send_web3_tx
from getpass import getpass

ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0x7461235dA33e9356a4b69B7e7b8686531d67EC75"
BYTECODE = "0x600a600c600039600a6000f3602a60005260206000f3"


def main():
    # setting up user
    user = accounts.load("YOUR_ALIAS")
    passphrase = getpass(f"Enter passphrase to permanently unlock {user.alias}: ")
    user.set_autosign(
        enabled=True, passphrase=passphrase
    )  # make sure you are on testnet

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    # deploy hacker contract
    print("\n--- Deploying hacker contract ---\n")
    hacker = project.MagicNumber.deploy(instance, sender=user)

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")
    receipt = send_web3_tx(BYTECODE, user, passphrase)

    # extract solver address from receipt
    solver = receipt.contractAddress

    # call attack function
    hacker.attack(solver, sender=user)

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()