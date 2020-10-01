import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from textwrap import dedent

"""
This project was inspired by https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
I have always had an interest in Blockchain as I learned about it in my security class. I wanted to get a better idea of how one worked as well
as work with flask.
"""
class blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        # Creating the new genesis block
        self.new_block(previous_hash=1, proof=100)
    
    # Creates a new block and adds it to the chain
    def new_block(self, proof, previous_hash):
        """
        Create a new block in the blockchain
        : param proof: <int> The proof given by the Proof of work algorithm
        : param previous_hash: (optional) <str> Hash of previous block
        return: <dick> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    # adds a new transaction to the list of transactions
    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined block
        : param sender: <str> Address of the Sender
        : param recipient: <str> Address of the Recipient
        : param amount: <int> amount
        : return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    # hashes a block
    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block
        :param block: <dict> block
        :return: <str>
        """

        # Must make sure the dictionary is ordered or else there will be inconsistent hashes
        block_string = json.dump(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Simple proof of work algorithm:
        - Find a number p such that hash(pp') contains 4 leading zeroes, where p' is the previous proof
        : param last_proof: <int>
        : return :< int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof: Does hash(last_proof, proof) contain four leading zeroes
        : param last_proof: <int> previous proof
        : param proof: <int> current proof
        : return: <bool> True if hash(last_proof, proof) contains four leading zeroes
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


    # returns the last block in the chain
    @property
    def last_block(self):
        return self.chain[-1]

# instantiate the flask node
app = Flask(__name__)

# Generate a globally unique address for the node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the blockchain
blockchain = blockchain()

########
# API
########

# route for mining a new block
@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    coin.blockchain.new_transaction(sender="0", recipient=node_identifier,amount=1,)

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', method=['POST'])
def new_transaction():
    values = request.get_json()
    if not validateTransaction(values):
        return "Properly formated request contains sender <String>, recipient<String>, and amount<int>", 400
    
    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


# Validates the values passed
def validateTransaction(values):
    if not isinstance(values['sender'], str):
        return False
    if not isinstance(values['recipient'], str):
        return False
    if not isinstance(values['amount'], int):
        return False
    return True


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)