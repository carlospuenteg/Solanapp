import os
import json

########## INSTALL SOLANA IF NEEDED ##########
if os.system("solana --version") != 0:
    os.system("sh -c '$(curl -sSfL https://release.solana.com/v1.9.4/install)'")



########## CREATE A WALLET ########## os.popen("spl-token create-token --decimals " + dec).read().split("\n")[0].split(" ")[2]
def createWallet():
    # Get last wallet number
    wallets = os.listdir('Wallets')
    keyNum = 1
    if wallets: 
        keyNum = max(sorted([int(keypair[6:]) for keypair in wallets]))+1

    # Create a key
    dir = "Wallets/Wallet" + str(keyNum)
    os.mkdir(dir)
    output = os.popen("solana-keygen new --no-passphrase -o " + dir + "/key.json").read().split("\n")

    # Save the seedPhrase and pubKey as a json file
    pubKey = output[3].split(" ")[1]
    seedPhrase = output[6]
    seed = { 
        "pubKey": pubKey, 
        "seedPhrase": seedPhrase 
    }
    with open(dir+"/seed.json", 'w') as json_file:
        json.dump(seed, json_file, indent=4)

    # Create a token folder
    os.mkdir(dir + "/Tokens")

    print("\nWallet successfully created!")



########## CREATE WALLET IF NEEDED ##########
if not os.listdir('Wallets'): createWallet()



########## GET THE SETTINGS ##########
config = json.load(open('Config/config.json'))
selWallet = config['wallet']
selCluster = config['cluster']
selBalance = config['balance']

seed = json.load(open("Wallets/Wallet" + str(selWallet) + "/seed.json"))
selPubKey = seed['pubKey']
os.system("solana config set --url https://api." + selCluster + ".solana.com")
os.system("solana config set --keypair " + "Wallets/Wallet" + str(selWallet) + "/key.json")
    



########## CREATE A CUSTOM KEY ##########
def customPubKey():
    getSeed = input("Do you want to get a seed for the key? (It will take much more time to find a key) (Y/n): ").lower()
    if getSeed == "y": getSeed = "--use-mnemonic "
    else: getSeed = ""

    keyLoc = input("Will your key START (s) or END (e) with ___ ? : ").lower()
    keyTxt = input("Text your key will contain: ")
    if keyLoc == "s":
        os.system("solana-keygen grind --starts-with " + keyTxt + ":1") # solana-keygen grind --starts-with e1v1s:1 -C ~/Wallets/hey.json
    elif keyLoc == "e":
        os.system("solana-keygen grind " + getSeed + "--ends-with " + keyTxt + ":1") # solana-keygen grind --starts-with e1v1s:1 -C ~/Wallets/hey.json
    print("\nThe key was saved in this folder")



########## CREATE A TOKEN ##########
def createToken():
    dec = input("Decimal places of the token: ")
    
    # Create a token and your account for the token
    tokenID = os.popen("spl-token create-token --decimals " + dec).read().split("\n")[0].split(" ")[2]
    account = os.popen("spl-token create-account " + tokenID).read().split("\n")[0].split(" ")[2]

    # Save the token ID
    if os.popen("solana balance " + account).read().split() != "0 SOL".split():
        dir = "Wallets/Wallet" + str(selWallet) + "/Tokens"
        tokens = os.listdir(dir)
        tokenNum = 1
        if tokens: 
            tokenNum = max(sorted([int(token[5:][:-5]) for token in tokens]))+1
        
        with open(dir + "/token" + str(tokenNum) + ".json", 'w') as json_file:
            json.dump({"tokenID": tokenID, "account": account}, json_file, indent=4)


########## GET YOUR ACCOUNT BALANCE ##########
def getBalance():
    if selBalance == "lamports":
        os.system("solana balance --lamports " + selPubKey)
    else:
        os.system("solana balance " + selPubKey)



########## AIRDROP SOLANA TO DEVNET ACCOUNT ##########
def airdrop():
    if selCluster == "devnet":
        while True:
            qty = input("Quantity (up to 2): ")
            if float(qty) <= 2:
                os.system("solana airdrop " + qty + " " + selPubKey + " --url https://api.devnet.solana.com")
                break
            else:
                print("- Invalid quantity")
    else:
        print("\nYou can't use airdrop in the mainnet")



########## MENU ##########
def menu():
    print("\nChoose an option: ")
    print("0. EXIT")
    print("1. Create a wallet")
    print("2. Create a custom public key")
    print("3. Get account balance")
    print("4. Airdrop solana (only for devnet)")
    print("5. Create a token")

    while True:
        op = input("\nOption: ")
        if op == "1": createWallet()
        elif op == "2": customPubKey()
        elif op == "3": getBalance()
        elif op == "4": airdrop()
        elif op == "5": createToken()



########## CALL THE MAIN FUNCTION ##########

menu()