from web3 import Web3
import requests

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
PINATA_API_KEY = 'b33bb9fd3b1e4695720c'
PINATA_API_SECRET = 'c94a351ca21b961981803374c091bb9fbc733e0869af09b2a46acafbd0a6f071'

contract_abi =[
    {
        "inputs": [],
        "name": "getHashes",
        "outputs": [
            {
                "internalType": "string[]",
                "name": "",
                "type": "string[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_hashToCheck",
                "type": "string"
            }
        ],
        "name": "isHashMatch",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_ipfsHash",
                "type": "string"
            }
        ],
        "name": "storeHash",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "ipfsHashes",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

contract_address = "0x9064858b9f6D1717F7A660AcCCC6dEE6418d30b1" 

def store_ipfs_hash(ipfs_hash):
    if not ipfs_hash:
        print("No IPFS hash provided, skipping blockchain storage.")
        return
    try:
        if not web3.is_connected():
            raise Exception("Failed to connect to the blockchain")

        contract = web3.eth.contract(address=contract_address, abi=contract_abi)
        account = web3.eth.accounts[0]  
        
        if not account:
            raise Exception("No account found in Ganache")
        else:
            print(f"Using account: {account}")

        tx_hash = contract.functions.storeHash(ipfs_hash).transact({'from': account})
        web3.eth.wait_for_transaction_receipt(tx_hash)
    except Exception as e:
        print(f"Error storing IPFS hash on blockchain: {e}")


def upload_to_pinata(file_path):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_API_SECRET
    }

    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files, headers=headers)
        
        if response.status_code == 200:
            ipfs_hash = response.json().get('IpfsHash')
            if ipfs_hash:
                print(f"Successfully uploaded to Pinata. IPFS Hash: {ipfs_hash}")
                return ipfs_hash
            else:
                raise Exception("Pinata response did not contain an IPFS hash")
        else:
            raise Exception(f"Failed to upload to Pinata. Status code: {response.status_code}. Response: {response.text}")
    
    except Exception as e:
        print(f"Error uploading file to Pinata: {e}")
        return None
