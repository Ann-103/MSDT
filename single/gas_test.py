import json
from collections import defaultdict
import hashlib
from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_account.messages import encode_defunct
from deploy import deploy_off_chain
from requestService import request_service
from cloudInit import cloud_init
from cloudArbitrate import cloud_arbitrate
from cloudTerminate import cloud_terminate
from clientTerminate import client_terminate
import time


def generate_testArgs(account_client,account_cloud,setNum):
    s1 = "key1"
    s2 = "key2"
    with open('wallet/rpc.json', 'r') as f:
        acc = json.load(f)
        rpc = acc['rpc']    
    web3 = Web3(Web3.HTTPProvider(rpc))
    message = encode_defunct(text=s1)
    signed_message = web3.eth.account.sign_message(message, private_key=account_client['private_key'])
    hashOfS1 = signed_message["messageHash"].hex()
    sig = signed_message["signature"].hex()
    
    sha256 = hashlib.new("sha256")
    sha256.update(str.encode(s2))
    verifyResult_i = eval(hashOfS1) ^ eval("0x" + sha256.hexdigest())
    newResult = hex(verifyResult_i)
    verifyResult = [newResult for i in range(setNum)]
    paySeed = "19b25856e1c150ca834cffc8b59b23adbd0ec0389e58eb22b3b64768098d002b"
    payHash = bytes.fromhex((paySeed))
    for i in range(setNum):
        sha256 = hashlib.new("sha256")
        sha256.update(payHash)
        payHash = sha256.digest()
    paySeed = "0x" + paySeed
    payHash = "0x" + sha256.hexdigest()
    args = defaultdict()
    args["account_client"] = account_client
    args["account_cloud"] = account_cloud
    args["s1"] = s1
    args["s2"] = s2
    args["verifyResult"] = verifyResult
    args["numOfSet"] = setNum
    args["setSeq"] = [i for i in range(setNum)]
    args["payNum"] = setNum
    args["payHash"] = payHash
    args["paySeed"] = paySeed
    args["setNum"] = setNum
    args["hashOfS1"] = hashOfS1
    args["sig"] = sig
    args["newResult"] = newResult
    json_str = json.dumps(args,indent = 4)
    with open('args.json', 'w') as json_file:
        json_file.write(json_str)
    return args


def test_cloudTerminate(args,args_c,contract_address):
    cloud_init(args["account_cloud"],contract_address,args_c["penalty"],args["verifyResult"])
    request_service(args["account_client"], contract_address, args_c["serviceFee"] * args["setNum"], args["setSeq"], args["payNum"], args["payHash"])
    cloud_terminate(args["account_cloud"], contract_address, 0, args["paySeed"], args["setNum"])


def test_clientTerminate(args,args_c,contract_address):
    cloud_init(args["account_cloud"],contract_address,args_c["penalty"],args["verifyResult"])
    request_service(args["account_client"], contract_address, args_c["serviceFee"] * args["setNum"], args["setSeq"], args["payNum"], args["payHash"])
    client_terminate(args["account_client"], contract_address, 0)
    

def test_cloudArbitrate(args,args_c,contract_address):
    cloud_init(args["account_cloud"],contract_address,args_c["penalty"],args["verifyResult"])
    request_service(args["account_client"], contract_address, args_c["serviceFee"] * args["setNum"], args["setSeq"], args["payNum"], args["payHash"])
    cloud_arbitrate(args["account_cloud"], contract_address, 0, args["s2"], args["hashOfS1"], args["sig"], args["setNum"], args["newResult"])


def test_all(_setNum):
    with open('wallet/client.json', 'r') as f:
        acc = json.load(f)
        account_client = acc     
    with open('wallet/cloud.json', 'r') as f:
        acc = json.load(f)
        account_cloud = acc 
    setNum = _setNum
    penalty = 0
    serviceFee = 1
    serviceTime = 123123
    args_c = dict()
    args_c["penalty"] = penalty
    args_c["serviceFee"] = serviceFee
    args_c["setNum"] = setNum

    args = generate_testArgs(account_client,account_cloud,setNum)
    # test cloudTerminate
    contract_address = deploy_off_chain(account_cloud,penalty,serviceFee,serviceTime,setNum)
    test_cloudTerminate(args,args_c,contract_address)
    print("")
    # test cloudArbitrate
    contract_address = deploy_off_chain(account_cloud,penalty,serviceFee,serviceTime,setNum)
    test_cloudArbitrate(args,args_c,contract_address)  
    print("")  
    # test clientTerminate
    serviceTime = 0
    contract_address = deploy_off_chain(account_cloud,penalty,serviceFee,serviceTime,setNum)
    test_clientTerminate(args,args_c,contract_address)
    print(_setNum,"---------------end-----------------")

if __name__ == "__main__":
    test_all(1)
    for i in range(5):
        test_all(5*i+5)
    
    
