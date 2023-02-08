from ape import networks, project
import subprocess

MAX_UINT256 = 2**256 - 1
w3 = networks.provider.web3


def get_level_instance(ethernaut, level, user, value="0 wei", gas=2000000):
    print("\n--- Creating level instance ---\n")
    ethernaut = project.Ethernaut.at(ethernaut)
    create_tx = ethernaut.createLevelInstance(
        level,
        sender=user,
        value=value,
        gas=gas,
    )
    instance = [
        log.instance
        for log in ethernaut.LevelInstanceCreatedLog.from_receipt(create_tx)
    ][0]
    print(f"\n--- Level Instance: {instance} ---\n")
    return instance, ethernaut


def level_completed(ethernaut, receipt, user, instance, level):
    assert len(receipt.logs) != 0, "\n--- !Level not passed! ---\n"
    logs = [log for log in ethernaut.LevelCompletedLog.from_receipt(receipt)][0]
    assert (
        logs.player == user and logs.instance == instance and logs.level == level
    ), "\n--- !something went wrong! ---\n"


def deploy_huff_contract(huff_contract, user):
    bytecode = subprocess.getoutput(f"huffc -b ./contracts/utils/{huff_contract}")
    txn = networks.ecosystems["arbitrum"].create_transaction(data=bytecode, gas=2000000)
    receipt = user.call(txn)
    return receipt.contract_address
