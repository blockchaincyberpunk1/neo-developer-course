import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, proof):
        """
        Constructor for the Block class.
        :param index: Unique index for the block.
        :param previous_hash: Hash of the previous block.
        :param timestamp: Timestamp of block creation.
        :param data: Data or transactions to be stored in the block.
        :param proof: Proof of work value for consensus.
        """
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.proof = proof

    def calculate_hash(self):
        """
        Calculate the SHA-256 hash of the block.
        :return: Hexadecimal hash string.
        """
        data = str(self.index) + self.previous_hash + str(self.timestamp) + str(self.data) + str(self.proof)
        return hashlib.sha256(data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        """
        Constructor for the Blockchain class.
        Initializes the blockchain with a genesis block.
        """
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Create the first block (genesis block) manually.
        """
        genesis_block = Block(0, "0", int(time.time()), "Genesis Block", 0)
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    def get_latest_block(self):
        """
        Get the latest block in the blockchain.
        :return: The latest Block object.
        """
        return self.chain[-1]

    def add_block(self, data, proof):
        """
        Add a new block to the blockchain.
        :param data: Data or transactions to be stored in the new block.
        :param proof: Proof of work value for consensus.
        """
        previous_block = self.get_latest_block()
        index = previous_block.index + 1
        timestamp = int(time.time())
        previous_hash = previous_block.hash
        new_block = Block(index, previous_hash, timestamp, data, proof)
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

# Example usage:
if __name__ == "__main__":
    blockchain = Blockchain()
    
    # Adding sample transactions
    blockchain.add_block("Transaction 1", proof=12345)
    blockchain.add_block("Transaction 2", proof=67890)
    
    # Display the blockchain
    for block in blockchain.chain:
        print(f"Block #{block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Proof: {block.proof}")
        print(f"Block Hash: {block.calculate_hash()}")
        print("\n")
