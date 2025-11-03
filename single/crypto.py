from Crypto.Hash import SHA256
import hashlib
import json
from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_account.messages import encode_defunct

account_from = {
        'private_key': '0xec3a78dd97c64dd2ac5f7ded230e05d1c65b7efed8ee0084f059e01b5e63b449',
        'address': '0xf8cCd42A7BD8fF3C5B5BcA4dB7B5d69fAad62E21',
    }
contract_address = '0x7db1dac839fD4477D9ad8fe34b9B099BD8350457'
value = 0
with open('wallet/rpc.json', 'r') as f:
        acc = json.load(f)
        rpc = acc['rpc']    
web3 = Web3(Web3.HTTPProvider(rpc))
message = encode_defunct(text="1")
print(message)
signed_message = web3.eth.account.sign_message(message, private_key=account_from['private_key'])
print(signed_message)
signed_message = web3.eth.sign(account_from["address"],text = "1")
print(signed_message)


# s = 0x6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b
# s2 = 0xd65fc3b188dd92cfcb2a193a50840c1b782030fb06c5eee3125dadc48b9042ee
# print(hex(s ^ s2))

# a = "19b25856e1c150ca834cffc8b59b23adbd0ec0389e58eb22b3b64768098d002b"
# print(bytes.fromhex((a)))

# payNum = 1
# paySeed = "19b25856e1c150ca834cffc8b59b23adbd0ec0389e58eb22b3b64768098d002b"
# payHash = bytes.fromhex((paySeed))
# for i in range(payNum):
#         sha256 = hashlib.new("sha256")
#         sha256.update(payHash)
#         payHash = sha256.digest()
# paySeed = "0x" + paySeed
# payHash = "0x"+ sha256.hexdigest()
# print(paySeed,payHash)

sha256 = hashlib.new("sha256")
sha256.update(b'1')
sha256.hexdigest()
print(eval("0x" + sha256.hexdigest()))