def load(hex_string):
    """Convert a hex string to a bytes object."""
    return bytes.fromhex(hex_string)

def otp(data, key):
    """Perform XOR between data and key."""
    return bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))

# Load the data and key from hex strings
data = load("15b279d8c0fdbd7d4a8eea255876a0fd189f4fafd4f4124dafae47cb20a447308e3f77995d3c")
key = load("73de18bfbb99db4f7cbed3156d40959e7aac7d96b29071759c9b70fb18947000be5d41ab6c41")

# Perform OTP
bytes_result = otp(data, key)

# Convert the result to a UTF-8 string
result_string = bytes_result.decode('utf-8', errors='ignore')

print(result_string)
