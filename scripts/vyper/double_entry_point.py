from ape import accounts, project
from ..utils.helper import get_level_instance, level_completed

ETHERNAUT = "0xD2e5e0102E55a5234379DD796b8c641cd5996Efd"
LEVEL = "0x9451961b7Aea1Df57bc20CC68D72f662241b5493"


def main():
    # setting up user
    user = accounts.test_accounts[0]

    # get level instance
    instance, ethernaut = get_level_instance(ETHERNAUT, LEVEL, user, gas=12_500_000)

    # deploy bot contract
    print("\n--- Deploying and Registering Bot Contract with Forta ---\n")
    bot = project.DoubleEntryPoint.deploy(instance, sender=user)
    forta = project.Forta.at(bot.forta())
    forta.setDetectionBot(bot, sender=user)

    assert forta.usersDetectionBots(user) == bot

    # submiting level instance
    print("\n--- Submitting level instance ---\n")
    submit_tx = ethernaut.submitLevelInstance(instance, sender=user)

    # checking if level is completed
    level_completed(ethernaut, submit_tx, user.address, instance, LEVEL)

    print("\n--- 🥂!LEVEL COMPLETED!🥂 ---\n")


if __name__ == "__main__":
    main()
