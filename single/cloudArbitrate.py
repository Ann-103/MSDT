import json
import hashlib
from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount


def cloud_arbitrate(account_from, contract_address, value, s2, hashOfS1, sig, setNum, newResult):
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
    init_tx = trading_contract.functions.cloudArbitrate(s2, hashOfS1, sig, setNum, newResult).build_transaction(
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
    print("cloudArbitrate:",tx_receipt["gasUsed"])

    init_tx = trading_contract.functions.restart().build_transaction(
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
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("restart:",tx_receipt["gasUsed"])

    return 0

if __name__ == "__main__":
    account_from = {
            'private_key': '0xec3a78dd97c64dd2ac5f7ded230e05d1c65b7efed8ee0084f059e01b5e63b449',
            'address': '0xf8cCd42A7BD8fF3C5B5BcA4dB7B5d69fAad62E21',
        }
    contract_address = '0x1671A1392bbfb66b96042D1fd253089B15e74D81'
    value = 0
    hashOfS1 = "0xd65fc3b188dd92cfcb2a193a50840c1b782030fb06c5eee3125dadc48b9042ee"
    s2 = "1"
    hashOfS1 = "0xd65fc3b188dd92cfcb2a193a50840c1b782030fb06c5eee3125dadc48b9042ee"
    sig = "0x269dcc7a1f307d7eb709d1697a76856147ad5f7dbe0d987f4e989be4410fc1b154e10a90a94d4308083570a7a71314a5180c4e1257511cdcabc32eeb1ffc00221b"
    setNum = 1
    
    sha256 = hashlib.new("sha256")
    sha256.update(b'1')
    hashOfS1 = "0xd65fc3b188dd92cfcb2a193a50840c1b782030fb06c5eee3125dadc48b9042ee"
    verifyResult_i = eval(hashOfS1) ^ eval("0x" + sha256.hexdigest())
    newResult = hex(verifyResult_i)
    cloud_arbitrate(account_from, contract_address, value, s2, hashOfS1, sig, setNum, newResult)
