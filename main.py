import os
import json

########## INSTALL SOLANA IF NEEDED ##########
if os.system("solana --version") != 0:
    os.system("sh -c '$(curl -sSfL https://release.solana.com/v1.9.4/install)'")



########## CREATE A WALLET ##########
def createWallet():
    config = json.load(open('config.json'))
    while True:
        wallName = input("Wallet's name: ")
        if "Wallets" not in os.listdir(os.getcwd()) or wallName not in os.listdir("Wallets"):
            break
        else:
            print("That name already exists!")

    if "Wallets" not in os.listdir(os.getcwd()):
        os.mkdir("Wallets")
        config['wallet'] = wallName 
        with open("config.json", 'w') as json_file:
            json.dump(config, json_file, indent=4)
    elif input("Do you want to select this wallet as your main wallet? (Y/n): ").lower() == "y":
        config['wallet'] = wallName 
        with open("config.json", 'w') as json_file:
            json.dump(config, json_file, indent=4)

    os.mkdir("Wallets/" + wallName)
    output = os.popen("solana-keygen new --no-passphrase -o Wallets/" + wallName + "/key.json").read().split("\n")
    pubKey = output[3].split(" ")[1]
    seedPhrase = output[6]
    seed = { 
        "pubKey": pubKey, 
        "seedPhrase": seedPhrase 
    }
    with open("Wallets/" + wallName + "/seed.json", 'w') as json_file:
        json.dump(seed, json_file, indent=4)

    print("\nWallet successfully created!")



########## CREATE WALLET IF NEEDED ##########
if "Wallets" not in os.listdir(os.getcwd()): 
    createWallet()



########## GET THE SETTINGS ##########
config = json.load(open('config.json'))
selWallet = config['wallet']
selCluster = config['cluster']
selBalance = config['balance']

seed = json.load(open("Wallets/" + selWallet + "/seed.json"))
selPubKey = seed['pubKey']
os.system("solana config set --url https://api." + selCluster + ".solana.com")
os.system("solana config set --keypair " + "Wallets/" + selWallet + "/key.json")
    



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
        tokenName = input("Name of the token: ")

        if "tokens.json" not in os.listdir(os.getcwd()):
            with open('tokens.json', 'w') as json_file:
                json.dump({}, json_file, indent=4)

        tokens = json.load(open('tokens.json'))
        tokens[tokenName] = tokenID

        with open("tokens.json", 'w') as json_file:
            json.dump(tokens, json_file, indent=4)
    else:
        print("\nUnable to create the token, insufficient balance")



########## CREATE AN ACCOUNT ##########
def createAccount():    
    tokens = json.load(open('tokens.json'))
    tokenName = input("Token name: ")
    tokenID = tokens[tokenName]
    os.system("spl-token create-account " + tokenID)



########## MINT TOKENS ##########
def mintTokens():
    tokens = json.load(open('tokens.json'))
    tokenName = input("Token name: ")
    tokenID = tokens[tokenName]
    qty = input("Quantity of tokens to be minted: ")
    os.system("spl-token mint " + tokenID + " " + qty)



########## DISABLE MINT ##########
def disableMint():
    tokens = json.load(open('tokens.json'))
    tokenName = input("Token name: ")
    tokenID = tokens[tokenName]
    os.system("spl-token authorize " + tokenID + " mint --disable")



########## TRANSFER TOKEN ##########
def tokenTransfer():
    tokens = json.load(open('tokens.json'))
    tokenName = input("Token name: ")
    tokenID = tokens[tokenName]
    qty = input("Quantity: ")
    receiver = input("Public key of the receiver: ")
    os.system("spl-token transfer --fund-recipient " + tokenID + " " + qty + " " + receiver + " --allow-unfunded-recipient")



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
            qty = input("Quantity: ")
            if float(qty) <= 2:
                os.system("solana airdrop " + qty + " " + selPubKey + " --url https://api.devnet.solana.com")
                break
            else:
                for x in range(int(float(qty)//2)):
                    os.system("solana airdrop 2 " + selPubKey + " --url https://api.devnet.solana.com")
                if (float(qty)%2):
                    os.system("solana airdrop " + str(float(qty)%2) + " " + selPubKey + " --url https://api.devnet.solana.com")
                break    
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
    print("6. Create a token account")
    print("7. Mint tokens")
    print("8. Disable minting of token")
    print("9. Transfer tokens")

    while True:
        op = input("\nOption: ")
        if op == "1": createWallet()
        elif op == "2": customPubKey()
        elif op == "3": getBalance()
        elif op == "4": airdrop()
        elif op == "5": createToken()
        elif op == "6": createAccount()
        elif op == "7": mintTokens()
        elif op == "8": disableMint()
        elif op == "9": tokenTransfer()



########## CALL THE MAIN FUNCTION ##########

menu()