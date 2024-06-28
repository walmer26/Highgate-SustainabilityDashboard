import hashlib

class HashManager:
    def __init__(self):
        self.existing_hashes = set()

    def generate_file_hash(self, file_path):
        """
        Generate a SHA-256 hash for the given file.
        
        Args:
            file_path (str): Path to the file.
        
        Returns:
            str: SHA-256 hash of the file.
        """
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    @staticmethod
    def generate_record_hash(**fields):
        """
        Generate a SHA-256 hash for the given record.
        
        Args:
            **fields: Arbitrary keyword arguments representing record fields.
        
        Returns:
            str: SHA-256 hash of the concatenated field values.
        """
        # Convert all field values to strings and concatenate them
        record_str = ''.join([str(value) for key, value in sorted(fields.items())])
        return hashlib.sha256(record_str.encode('utf-8')).hexdigest()

    def check_duplicate(self, file_hash):
        """
        Check if the file hash already exists in the set of existing hashes.
        
        Args:
            file_hash (str): Hash to check.
        
        Returns:
            bool: True if the hash exists, False otherwise.
        """
        return file_hash in self.existing_hashes

    def add_hash(self, file_hash):
        """
        Add a new file hash to the set of existing hashes.
        
        Args:
            file_hash (str): Hash to add.
        """
        self.existing_hashes.add(file_hash)

