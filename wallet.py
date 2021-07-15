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
    coins[coin].append(derive_wallets(mnemonic,coin,3))

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
#def priv_key_to_account(coin, priv_key):
    # YOUR CODE HERE

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
#def create_tx(coin, account, to, amount):
    # YOUR CODE HERE

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
#def send_tx(coin, account, to, amount):
    # YOUR CODE HERE

print(coins)
