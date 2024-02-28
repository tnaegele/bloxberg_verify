#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This script verifies the integrity of a Bloxberg timestamp generated on https://certify.bloxberg.org/.
Script needs as only argument the bloxbergJSONCertificate.json file which is embedded in the proof pdf.
It can for example be extracted with poppler's pdfdetach -saveall doc.pdf.


@author: Tobias E. Naegele, 02/2024

Copyright (c) 2024 Tobias E. Naegele

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

__author__ = "Tobias E. Naegele"
__maintainer__ = __author__
__version__ = "1.0"
__email__ = "github@tobiasnaegele.com"

import hashlib
from pyld import jsonld
import json
from lds_merkle_proof_2019.merkle_proof_2019 import MerkleProof2019
import argparse
from web3 import Web3
import datetime
import sys


# contract details for bloxberg timestamps
CONTRACT_ADDRESS = '0x3fb704dfDB72Fc06860D9F09124C30919488f13C'
ABI = '[{"type":"constructor","stateMutability":"nonpayable","inputs":[]},{"type":"event","name":"Approval","inputs":[{"type":"address","name":"owner","internalType":"address","indexed":true},{"type":"address","name":"approved","internalType":"address","indexed":true},{"type":"uint256","name":"tokenId","internalType":"uint256","indexed":true}],"anonymous":false},{"type":"event","name":"ApprovalForAll","inputs":[{"type":"address","name":"owner","internalType":"address","indexed":true},{"type":"address","name":"operator","internalType":"address","indexed":true},{"type":"bool","name":"approved","internalType":"bool","indexed":false}],"anonymous":false},{"type":"event","name":"OwnershipTransferred","inputs":[{"type":"address","name":"previousOwner","internalType":"address","indexed":true},{"type":"address","name":"newOwner","internalType":"address","indexed":true}],"anonymous":false},{"type":"event","name":"Transfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":true},{"type":"address","name":"to","internalType":"address","indexed":true},{"type":"uint256","name":"tokenId","internalType":"uint256","indexed":true}],"anonymous":false},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"approve","inputs":[{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"tokenId","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"owner","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"baseURI","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"createCertificate","inputs":[{"type":"address","name":"recipient","internalType":"address"},{"type":"string","name":"tokenURI","internalType":"string"},{"type":"string","name":"tokenHash","internalType":"string"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"getApproved","inputs":[{"type":"uint256","name":"tokenId","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"isApprovedForAll","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"address","name":"operator","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"name","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"owner","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"ownerOf","inputs":[{"type":"uint256","name":"tokenId","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"renounceOwnership","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"safeTransferFrom","inputs":[{"type":"address","name":"from","internalType":"address"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"tokenId","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"safeTransferFrom","inputs":[{"type":"address","name":"from","internalType":"address"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"tokenId","internalType":"uint256"},{"type":"bytes","name":"_data","internalType":"bytes"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setApprovalForAll","inputs":[{"type":"address","name":"operator","internalType":"address"},{"type":"bool","name":"approved","internalType":"bool"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"supportsInterface","inputs":[{"type":"bytes4","name":"interfaceId","internalType":"bytes4"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"symbol","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"tokenByIndex","inputs":[{"type":"uint256","name":"index","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"tokenHash","inputs":[{"type":"uint256","name":"tokenId","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"tokenOfOwnerByIndex","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"uint256","name":"index","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"tokenURI","inputs":[{"type":"uint256","name":"tokenId","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"transferFrom","inputs":[{"type":"address","name":"from","internalType":"address"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"tokenId","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"transferOwnership","inputs":[{"type":"address","name":"newOwner","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"updateTokenURI","inputs":[{"type":"uint256","name":"tokenID","internalType":"uint256"},{"type":"string","name":"tokenURI","internalType":"string"}]}]'


parser = argparse.ArgumentParser()
def init_argparse():
    parser = argparse.ArgumentParser(
        prog='originstamp_verify',
        description='Verifies an Originstamp blockchain timestamp pdf proof. Currently only Bitcoin timestamps are supported and script can only verify pdf proofs.')
    parser.add_argument(
        'file', help='Originstamp proof pdf file to be verified')
    return parser


def print_ok():
    '''
    Prints success message.

    Returns
    -------
    None.

    '''
    print('\033[92m success ✓ \033[0m')


def print_fail():
    '''
    Prints failure message.

    Returns
    -------
    None.

    '''
    print('\033[91m failure ✗\033[0m')


def calculate_merkle_root(json_proof):
    '''
    Calculates the merkle root from the content of the loaded json proof file
    procedure described on https://github.com/blockchain-certificates/cert-verifier-js/blob/master/docs/verification-process.md
    first, remove the 'proof' section from the json file for the hash calculation, then normalise json and calculate sha256 hash    

    Parameters
    ----------
    json_proof : dict
        'proof' field from Bloxberg proof json.

    Returns
    -------
    generated_merkle_root : str
        Calculated merkle root.
    normalized_proof : str
        Normalised proof.

    '''
    # remove 'proof' section
    json_proof.pop('proof')
    # canonicalize the json to get reproducible hashes
    normalized_proof = jsonld.normalize(
        json_proof, {'algorithm': 'URDNA2015', 'format': 'application/nquads'})

    # calculate sha256 hash of the normalized proof, this is the merkle root
    # embedded into the blockchain
    calculated_merkle_root = hashlib.sha256(
        str.encode(normalized_proof)).hexdigest()
    return calculated_merkle_root, normalized_proof


def extract_proof_data(proof_data):
    '''
    Extracts the merkle root and transaction hash saved in the encoded json proof file.

    Parameters
    ----------
    proof_data : dict
        Proof data from json file.

    Returns
    -------
    extracted_merkle_root : str
        Merkle root.
    transaction : str
        Transaction ID.

    '''

    mp2019 = MerkleProof2019()  # initialise lds_merkle proof package
    decoded_data = mp2019.decode(
        proof_data['proofValue'])  # decode the proof
    extracted_merkle_root = decoded_data['merkleRoot']
    transaction = decoded_data['anchors'][0].strip('blink::eth::')
    return extracted_merkle_root, transaction


def check_blockchain(txn_id):
    '''
    Extracts merkle root 'tokenHash' from bloxberg contract call with transaction id txn_id
    returns the merkle root stored in the blockchain, the timestamp and the number of block confirmations

    Parameters
    ----------
    txn_id : str
        Transaction ID to be checked on blockchain.

    Raises
    ------
    ConnectionError
        Connection error if Bloxberg server not reachable.

    Returns
    -------
    web_mr : str
        Merkle root stored in the blockchain for requested transaction id.
    timestamp : int
        Timestamping time as UNIX timestamp.
    confirms : int
        Number of confirmation of block.

    '''
    w3 = Web3(Web3.HTTPProvider('https://core.bloxberg.org/'))
    if not w3.is_connected():
        raise ConnectionError()
    contract = w3.eth.contract(CONTRACT_ADDRESS, abi=ABI)
    txn = w3.eth.get_transaction(txn_id)
    web_mr = contract.decode_function_input(txn.input)[1]['tokenHash']

    timestamp = w3.eth.get_block(
        txn.blockNumber).timestamp  # get block timestamp
    # get number of block confirmations
    confirms = w3.eth.block_number - txn.blockNumber

    return web_mr, timestamp, confirms

def verify_file(file_path):
    '''
    Verifies Bloxberg json proof file.

    Parameters
    ----------
    file_path : str
        Path to Bloxberg json proof which is attached to the proof pdf.

    Returns
    -------
    int
        0 of successful.
    '''
    with open(file_path) as json_file:
        json_proof = json.load(json_file)
        # save the 'proof' section into a separate variable, do this now as .pop()
        # will change json_proof
        extracted_proof_data = json_proof['proof']
    
    calculated_mr, normalized_proof = calculate_merkle_root(json_proof)
    extracted_mr, transaction_id = extract_proof_data(extracted_proof_data)
    transaction_id = transaction_id.split(':')[1]
    original_file_hash = json_proof['crid']
    # timestamp = json_proof['issuanceDate']
    
    # check if document hash is actually in the normalised proof, this used to
    # be a bug so be extra safe
    print('\n\nCheck that document hash is contained in normalised proof')
    if original_file_hash not in normalized_proof:
        print('Fatal error: document hash gets lost when normalising json. document hash not embedded in blockchain!')
        print_fail()
        exit(0)
    else:
        print_ok()
    
    print('Check file integrity, i.e. if the merkle root hash encoded in this file is identical to the calculated hash of this file.')
    if calculated_mr == extracted_mr:
        print_ok()
    
        print('\nOriginal file hash: ', original_file_hash)
        print('Merkle root: ', calculated_mr)
        print('Transaction id: ', transaction_id, '\n')
    
        print('Check if transaction exists in the blockchain and if it contains the merkle root')
        web_hash, timestamp, confirms = check_blockchain(transaction_id)
        if web_hash == calculated_mr:
            timestamp_readable = datetime.datetime.fromtimestamp(
                timestamp,datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')
            print_ok()
            print(f'Hashes match. The file is properly timestamped on the bloxberg blockchain. The block timestamp is {
                  timestamp_readable} and the number of block confirmations is {confirms}.')
        else:
            print('Error: hash in file and hash online do not match!')
            print_fail()
    
    else:
        print('Error: calculated file hash is not identical to extracted file hash. The json proof file has been tampered.')
        print_fail()
    return 0


if __name__ == '__main__':
    parser = init_argparse()
    args = parser.parse_args()
    file = args.file
    try:
        verify_file(file_path=file)
    except (FileNotFoundError, IsADirectoryError) as err:
        print(f"{sys.argv[0]}: {file}: {err.strerror}", file=sys.stderr)

