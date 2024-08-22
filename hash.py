import hashlib


def hash_generator(message):
    hash_object = hashlib.sha256(message.encode('utf-8'))
    hash_hex = hash_object.hexdigest()
    hash_decimal = int(hash_hex, 16)
    hash_value_ready = hash_decimal % (10 ** 8)
    print("The hash value generated")
    return hash_value_ready