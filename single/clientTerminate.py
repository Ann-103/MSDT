import json
import hashlib
from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount

def client_terminate(account_from, contract_address, value):
    with open('wallet/rpc.json', 'r') as f:
        acc = json.load(f)
        rpc = acc['rpc']    
    web3 = Web3(Web3.HTTPProvider(rpc))

    # 读取文件中的abi和bin,也可以当场生成
    with open('contract/Launchpad_metadata.json', 'r') as f:
        abi = json.load(f)
        abi = abi['output']['abi']
 
    with open('contract/Launchpad.json', 'r') as f:
        code = json.load(f)
        code = code['data']['bytecode']['object']

    trading_contract = web3.eth.contract(address=contract_address, abi=abi)
    # 发起交易部署合约
    option = {'from': account_from['address'], 'gas': 1000000}
    # web3.geth.personal.unlock_account(account, '123')
    # tx_hash = newContract.constructor(0, 0, 123123123,1).transact(option)
    init_tx = trading_contract.functions.clientTerminate().build_transaction(
        {
            "from": Web3.to_checksum_address(account_from["address"]),
            "nonce": web3.eth.get_transaction_count(
                Web3.to_checksum_address(account_from["address"])
            ),
            "value": value,
        }
    )
    tx_create = web3.eth.account.sign_transaction(
        init_tx, account_from["private_key"]
    )
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    # 等待挖矿使得交易成功

    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("clientTerminate:",tx_receipt["gasUsed"])

    # init_tx = trading_contract.functions.restart().build_transaction(
    # {
    #     "from": Web3.to_checksum_address(account_from["address"]),
    #     "nonce": web3.eth.get_transaction_count(
    #         Web3.to_checksum_address(account_from["address"])
    #     ),
    #     "value": value,
    #     }
    # )
    # tx_create = web3.eth.account.sign_transaction(
    #     init_tx, account_from["private_key"]
    # )
    # tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    # tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    # print("restart:",tx_receipt["gasUsed"])
    return 0

if __name__ == "__main__":
    account_from = {
            'private_key': '0xec3a78dd97c64dd2ac5f7ded230e05d1c65b7efed8ee0084f059e01b5e63b449',
            'address': '0xf8cCd42A7BD8fF3C5B5BcA4dB7B5d69fAad62E21',
        }
    contract_address = '0x1671A1392bbfb66b96042D1fd253089B15e74D81'
    value = 0
    client_terminate(account_from, contract_address, value)
