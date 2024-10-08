from django.shortcuts import render
from .forms import UploadFileForm
from .utils import upload_to_pinata, store_ipfs_hash ,contract_abi,contract_address,web3
import os
from web3 import Web3

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            
            uploaded_file = request.FILES['file']

            temp_file_path = f"/tmp/{uploaded_file.name}"
            with open(temp_file_path, 'wb+') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

            ipfs_hash = upload_to_pinata(temp_file_path)
            if not ipfs_hash:
                return render(request, 'upload_file.html', {'form': form, 'error': 'Failed to upload to Pinata'})

            try:
                store_ipfs_hash(ipfs_hash)
            except Exception as e:
                return render(request, 'upload_file.html', {'form': form, 'error': f'Blockchain storage failed: {str(e)}'})

            upload_dir = 'media/uploads/'
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            hash_file_path = os.path.join(upload_dir, f"{uploaded_file.name}_hash.txt")
            with open(hash_file_path, 'w') as hash_file:
                hash_file.write(f"{ipfs_hash}")
    
            return render(request, 'upload_success.html', {'hash': ipfs_hash})
    else:
        form = UploadFileForm()

    return render(request, 'upload_file.html', {'form': form})

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def check_hash(request):
    if request.method == 'POST':
        input_hash = request.POST.get('hash')

        try:
            is_match = contract.functions.isHashMatch(input_hash).call()

            if is_match:
                result = "The hash matches the stored hash on the blockchain."
            else:
                result = "The hash does not match the stored hash on the blockchain."

        except Exception as e:
            result = f"Error occurred: {str(e)}"

        return render(request, 'check_hash.html', {'result': result})

    return render(request, 'check_hash.html')