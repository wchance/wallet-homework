# Import dependencies
import subprocess
import json
from dotenv import load_dotenv
import os

# Load and set environment variables
load_dotenv('mnemonic.env')
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
from constants import *
from bit import PrivateKeyTestnet
#import web3
from web3 import Web3
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

#Trouble shoot if connected to node
#print(w3.isConnected())
  
# Create a function called `derive_wallets`
def derive_wallets(words, coin, num):
    command = 'php ./derive -g --mnemonic="' + words + '" --coin=' + coin + ' --numderive=' + str(num) + ' --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {BTCTEST:[],ETH:[]}
list = BTCTEST,ETH
for coin in list:
    coins[coin].extend(derive_wallets(mnemonic,coin,4))

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return w3.eth.accounts.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
    return None

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to, amount):
    if coin == ETH: 
        gasEstimate = w3.eth.estimateGas(
            {"from":eth_acc.address, "to": to, "value": amount}
        )
        return { 
            "from": eth_acc.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(eth_acc.address)
        }
    
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to, amount):
    txn = create_tx(coin, account, to, amount)
    if coin == ETH:
        signed_txn = eth_acc.sign_transaction(txn)
        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(result.hex())
        return result.hex()
    elif coin == BTCTEST:
        tx_btctest = create_tx(coin, account, recipient, amount)
        signed_txn = account.sign_transaction(txn)
        print(signed_txn)
        return NetworkAPI.broadcast_tx_testnet(signed_txn)


print(priv_key_to_account(ETH, '0x526ba7ad5543dbf0f8163f99966b7d43cedd49e9f0421ea8b45e76009c4e785b'))

#WORKS
#print(priv_key_to_account(BTCTEST, 'cRH5aKMLYrjNBkeFXBHmVyzjSR1wqfwMnxEh5QYyu9o2QiRtyFw8'))
