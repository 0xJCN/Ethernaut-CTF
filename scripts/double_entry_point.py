from ape import accounts, project
from .utils.helper import get_level_instance, level_completed

ETHERNAUT = "0xa3e7317E591D5A0F1c605be1b3aC4D2ae56104d6"
LEVEL = "0xb116e840ca8fC89CE05DAE6affC9c2040eb8E637"


def main():
    # setting up user
    user = accounts.load("YOUR_ALIAS")
    user.set_autosign(enabled=True)  # make sure you are on testnet

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
