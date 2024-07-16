import os
import base64

def hex_to_base64(hex_str):
    bytes_data = bytes.fromhex(hex_str)
    #base64_data = base64.b64encode(bytes_data)
    return bytes_data.decode()

def decode_base64(base64_str):
    bytes_data = base64.b64decode(base64_str)
    return bytes_data.decode()

def grep_content(directory, exclude_str="leveleffect{fake_flag}"):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as f:
                    hex_data = f.read().strip()
                    base64_data = hex_to_base64(hex_data)
                    #print(base64_data+"--------")
                    text_data = decode_base64(base64_data)
                    #print(text_data+"+++++")
                    if exclude_str != text_data:
                        print(f"File: {file_path}")
                        print(text_data)
                        print("-" * 80)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# Example usage
directory = 'haystack/'  # Change this to your target directory
grep_content(directory)
