// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IPFSStorage {
    string[] public ipfsHashes;  

    function storeHash(string memory _ipfsHash) public {
        ipfsHashes.push(_ipfsHash);  
    }
    function getHashes() public view returns (string[] memory) {
        return ipfsHashes;
    }

    function isHashMatch(string memory _hashToCheck) public view returns (bool) {
        for (uint i = 0; i < ipfsHashes.length; i++) {
            if (keccak256(abi.encodePacked(_hashToCheck)) == keccak256(abi.encodePacked(ipfsHashes[i]))) {
                return true;  
            }
        }
        return false;  
    }
}
