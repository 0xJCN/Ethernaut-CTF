from ape import networks, project


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


def send_web3_tx(calldata, user, passphrase, to="", gas=1000000):
    # prep args
    nonce = user.nonce
    chain_id = networks.provider.chain_id
    private_key = w3.eth.account.decrypt(user.keyfile, passphrase).hex()
    gas_price = networks.provider.gas_price
    # sign the transaction
    signed_tx = w3.eth.account.sign_transaction(
        dict(
            to=to,
            nonce=nonce,
            gas=gas,
            gasPrice=gas_price,
            value=0,
            data=calldata,
            chainId=chain_id,
        ),
        private_key,
    )
    # send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # wait for the receipt
    return w3.eth.wait_for_transaction_receipt(tx_hash)
