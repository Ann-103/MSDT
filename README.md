# MSDT: Blockchain-Based Multi-Subset Data Trading Protocol Enabled Data Availability and Non-repudiation

## Paper Performance Testing

Testing the gas costs of smart contracts designed in the paper by setting up a private Ethereum blockchain locally.

### Install dependencies

Run `pip install -r requirements.txt` to install the required Python libraries.

### Build a private blockchain

To set up a private Ethereum blockchain locally, you can use Truffle's Ganache component to accomplish this quickly.

### Create Account

Create two blockchain accounts and ensure sufficient funds in each account.

## On-Chain Gas Cost Testing

Write the two account addresses and private keys to `MSDT\single\wallet\client.json` and `MSDT\single\wallet\cloud.json`.

Write the local node RPC address to `MSDT\single\wallet\rpc.json`.

After enabling the private blockchain, navigate to the single directory and run `python gas_test.py` to complete the contract gas cost test.
