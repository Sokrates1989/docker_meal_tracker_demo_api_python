## Utilities for password/login like operations using hash algorithm.

# Import hash library to secure login-like behaviour.
import hashlib

# Get Sha512 hash of passed strings.
def getSha512(password, pepper, salt="CREATE YOUR OWN SALT like This one(just random chars, use UpperCase/lowercase, special chars and numbers preferable): aSDh7u8o134z5890712374ß9v571ß293vß9qe&123801348509134985§124889137"):
	stringToHash = password + pepper + salt
	hash_object = hashlib.sha512(stringToHash)
	hex_dig = hash_object.hexdigest()
	return hex_dig
