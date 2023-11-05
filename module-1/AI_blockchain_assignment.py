import hashlib
import json
import time

class Blockchain:
    def __init__(self):
        """
        Initialize the blockchain.
        """
        self.chain = []  # List to store blocks
        self.transactions = []  # List to store transactions in a block
        self.create_block(proof=1, previous_hash='0')  # Create the genesis block (first block)
        self.ai_model = AIModel()  # Initialize the AI model

    def create_block(self, proof, previous_hash):
        """
        Create a new block in the blockchain.

        :param proof: Proof of work for the new block
        :param previous_hash: Hash of the previous block
        :return: The new block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash,
        }
        self.transactions = []  # Clear transactions for the new block
        self.chain.append(block)
        return block

    def get_previous_block(self):
        """
        Get the previous block in the blockchain.

        :return: The previous block
        """
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """
        Perform proof of work to find a valid proof for a new block.

        :param previous_proof: Proof of the previous block
        :return: A valid proof
        """
        new_proof = 1
        while True:
            # Search for a hash with four leading zeros (customizable)
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                return new_proof
            new_proof += 1

    def add_transaction(self, sender, receiver, amount):
        """
        Add a new transaction to the list of transactions.

        :param sender: Sender's name
        :param receiver: Receiver's name
        :param amount: Transaction amount
        :return: The index of the block that will hold this transaction
        """
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return self.get_previous_block()['index'] + 1

    def is_chain_valid(self):
        """
        Check the validity of the entire blockchain.

        :return: True if the chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i - 1]
            current_block = self.chain[i]

            # Check if the hash of the current block matches the calculated hash
            if current_block['previous_hash'] != self.hash(previous_block):
                return False

            # Check if the proof of work is valid
            previous_proof = previous_block['proof']
            current_proof = current_block['proof']
            hash_operation = hashlib.sha256(
                str(current_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False

        return True

    @staticmethod
    def hash(block):
        """
        Calculate the SHA-256 hash of a block.

        :param block: The block to be hashed
        :return: The hash of the block
        """
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

class AIModel:
    def predict(self, transaction):
        """
        A simplified AI model that predicts the validity of a transaction.

        :param transaction: Transaction data
        :return: True if the transaction is valid, False otherwise
        """
        # In this simple example, we assume transactions under 100 are valid
        if transaction['amount'] < 100:
            return True
        return False

# Initialize the blockchain
blockchain = Blockchain()

# Example transactions
blockchain.add_transaction('Alice', 'Bob', 50)
blockchain.add_transaction('Bob', 'Charlie', 200)
blockchain.add_transaction('Alice', 'Eve', 75)

# Mining a new block
previous_block = blockchain.get_previous_block()
previous_proof = previous_block['proof']
proof = blockchain.proof_of_work(previous_proof)
previous_hash = blockchain.hash(previous_block)
blockchain.add_transaction('Miner', 'Alice', 1)  # Reward for mining
block = blockchain.create_block(proof, previous_hash)

# Example of AI integration (checking transaction validity)
latest_transaction = block['transactions'][-1]
is_valid_transaction = blockchain.ai_model.predict(latest_transaction)

# Print blockchain status
print("Blockchain:")
print(json.dumps(blockchain.chain, indent=2))

# Print AI prediction result
print("\nAI Prediction for the Latest Transaction:")
if is_valid_transaction:
    print("The latest transaction is predicted to be valid.")
else:
    print("The latest transaction is predicted to be invalid.")
