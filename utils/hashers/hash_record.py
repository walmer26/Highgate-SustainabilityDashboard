import hashlib


def hash_record(**fields):
    """
    This function is to hash any records to detect changes.
    It accepts any number of fields as keyword arguments.
    """
    # Convert all field values to strings and concatenate them
    record_str = ''.join([str(value) for key, value in sorted(fields.items())])
    return hashlib.sha256(record_str.encode('utf-8')).hexdigest()