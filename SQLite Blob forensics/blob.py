import sqlite3
import zlib
import re

# Function to find the starting point of zlib stream (78 9C)
def find_zlib_stream(data):
    # Search for the sequence 0x78 0x9C, which is the zlib stream start
    match = re.search(b'x\x9c', data, re.IGNORECASE)
    if match:
        return match.start()
    return None

# Connect to the SQLite database
db_file = 'ancient.fossil'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Query to get all the blob content
cursor.execute("SELECT content FROM blob")

# Set to store distinct decompressed content
distinct_data = set()

# Iterate over each row and decode the blob content
for row in cursor.fetchall():
    blob_content = row[0]

    try:
        binary_data = blob_content
        # Find the start of the zlib stream (78 9C)
        start_idx = find_zlib_stream(binary_data)

        if start_idx is not None:
            # Extract the zlib stream from the identified position
            zlib_data = binary_data[start_idx:]
            decompressed_data = zlib.decompress(zlib_data).decode()

            # Add the decompressed data to the set to ensure only distinct entries
            distinct_data.add(decompressed_data)

        else:
            print(f"No zlib stream found in this blob.")

    except Exception as e:
        print(f"Error processing blob: {e}")

# Close the database connection
conn.close()

# Output the distinct decompressed data
with open('decode_blob.txt','w') as f:
    for data in distinct_data:
        f.write(data)
        f.write('-'*40+'\n')
f.close()
tmp = []
for data in distinct_data:
    C = data.split("\n")[0]
    confi = C.split(" ")
    if confi[0] == 'C':
        if 'flag' in confi[1]:
            print("Found flag: {}".format(confi[1]))
    else:
        if 'flag' in confi[0]:
            print("Found flag: {}".format(confi[0]))
