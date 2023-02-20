from ape import networks, project
from eth_abi import encode
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


def get_sig(func):
    return subprocess.getoutput(f"cast sig '{func}'")


def deploy_huff_helper(huff_contract, user, gas=2000000):
    bytecode = subprocess.getoutput(f"huffc -b ./contracts/utils/{huff_contract}")
    txn = networks.ecosystems["ethereum"].create_transaction(data=bytecode, gas=gas)
    receipt = user.call(txn)
    return receipt.contract_address


def deploy_huff_contract(huff_contract, instance, user, value=0, gas=2000000):
    bytecode = subprocess.getoutput(f"huffc -b ./contracts/huff/{huff_contract}")
    deployment_code = bytecode + encode(["address"], [instance]).hex()
    txn = networks.ecosystems["ethereum"].create_transaction(
        data=deployment_code,
        gas=gas,
        value=value,
    )
    receipt = user.call(txn)
    return receipt.contract_address


def send_tx(sender, receiver, calldata, gas=2000000):
    txn = networks.ecosystems["ethereum"].create_transaction(
        to=receiver,
        data=calldata,
        gas=gas,
    )
    receipt = sender.call(txn)
    return receipt
