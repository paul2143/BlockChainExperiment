import hashlib
import json
from time import time


class blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.new_block(previous_hash=1, proof=100)
    
    # Creates a new block and adds it to the chain
    def new_block(self, proof, previous_hash):
        """
        Create a new block in the blockchain
        :param proof: <int> The proof given by the Proof of work algorithm
        :param previous_hash: (optional) <str> Hash of previous block
        return: <dick> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

    # adds a new transaction to the list of transactions
    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> amount
        :return: <int> The index of the Block that will hold this transaction
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


    # returns the last block in the chain
    @property
    def last_block(self):
        return self.chain[-1]
