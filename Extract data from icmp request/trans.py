from scapy.all import rdpcap, ICMP

def extract_icmp_data(pcap_file, request_file, response_file):
    # Read the PCAP file
    packets = rdpcap(pcap_file)

    # Open the output files for writing
    with open(request_file, 'w') as req_file, open(response_file, 'w') as res_file:
        for packet in packets:
            # Check if the packet has an ICMP layer
            if packet.haslayer(ICMP):
                # Get the ICMP layer
                icmp_layer = packet[ICMP]
                # Check if it's an Echo (ping) request or response
                if icmp_layer.type == 8:  # Type 8 is Echo request
                    if len(icmp_layer.payload) > 16:
                        # Skip the first 16 bytes and extract only the data part
                        data = bytes(icmp_layer.payload)[16:].hex()  # Convert to hex format
                        formatted_data = ' '.join(data[i:i+2] for i in range(0, len(data), 2))
                        # Write the formatted data to the request file
                        req_file.write(formatted_data + '\n')
                elif icmp_layer.type == 0:  # Type 0 is Echo reply
                    if len(icmp_layer.payload) > 16:
                        # Skip the first 16 bytes and extract only the data part
                        data = bytes(icmp_layer.payload)[16:].hex()  # Convert to hex format
                        formatted_data = ' '.join(data[i:i+2] for i in range(0, len(data), 2))
                        # Write the formatted data to the response file
                        res_file.write(formatted_data + '\n')

def compare_files(request_file, response_file):
    # Read the contents of both files
    with open(request_file, 'r') as req_file, open(response_file, 'r') as res_file:
        req_data = req_file.readlines()
        res_data = res_file.readlines()

    # Compare the contents line by line
    are_same = True
    for req_line, res_line in zip(req_data, res_data):
        if req_line.strip() != res_line.strip():
            are_same = False
            break

    if are_same:
        print(f'Contents of {request_file} and {response_file} are the same.')
    else:
        print(f'Contents of {request_file} and {response_file} are different.')

if __name__ == "__main__":
    # Specify your PCAP file and output files
    pcap_file = 'input.pcap'  # Change to your PCAP file path
    request_file = 'echo_requests.txt'
    response_file = 'echo_responses.txt'
    
    extract_icmp_data(pcap_file, request_file, response_file)
    print(f'Echo request data written to {request_file}')
    print(f'Echo response data written to {response_file}')
    
    # Compare the contents of the request and response files
    compare_files(request_file, response_file)
