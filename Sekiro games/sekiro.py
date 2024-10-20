import socket
import time
import re

# Define your response moves
responses = {
    "block": "block\n",  # Add newline to simulate pressing Enter
    "strike": "strike\n",
    "retreat": "retreat\n",
    "advance": "advance\n"
}

# Define your strategy based on opponent moves
def respond_to_opponent(opponent_move):
    if opponent_move == "block":
        return responses["advance"]  # Advance when they block
    elif opponent_move == "retreat":
        return responses["strike"]  # Strike when they retreat
    elif opponent_move == "advance":
        return responses["retreat"]  # Retreat when they advance
    elif opponent_move == "strike":
        return responses["block"]  # Block when they strike
    return None  # No valid move found

def main():
    # Set up the socket connection
    host = 'challenge.ctf.games'
    port = 32207

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Connected to netcat server. Waiting for opponent moves...")

        while True:
            try:
                output = s.recv(1024)
                if output:
                    # Debugging output: print the raw bytes received
                    #print(f"Raw output received: {output}")
                    # Attempt to decode the output
                    try:
                        decoded_output = output.decode('utf-8')
                        print(decoded_output)
                    except UnicodeDecodeError:
                        continue

                    # Check for the opponent's move
                    match_opponent = re.search(r"Opponent move: (\w+)", decoded_output)
                    match_me = re.search(r"Your move:", decoded_output)
                    
                    if match_opponent:
                        opponent_move = match_opponent.group(1)
                        response = respond_to_opponent(opponent_move)
                        
                        if response:
                            print(f"Responding with: {response.strip()}")
                            # Send the response when "Your move:" prompt is detected
                            if match_me:
                                s.sendall(response.encode('utf-8'))  # Send the response to the server
                            else:
                                print("Waiting for 'Your move' prompt before sending response.")
                        else:
                            print("No valid response found.")  # Handle case where response is None
            
                time.sleep(0.1)  # Small delay to avoid busy-waiting

            except Exception as e:
                print(f"An error occurred: {e}")
                break  # Exit the loop on error

if __name__ == "__main__":
    main()
