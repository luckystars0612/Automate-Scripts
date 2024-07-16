#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No color

# Check if a domain is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <domain>"
  exit 1
fi

# Define the target domain from the first argument
DOMAIN=$1
CLEANED_DOMAIN=$(echo $DOMAIN | sed 's|http[s]\?://||; s|/$||')

# Run ParamSpider and save output to params.txt
echo -e "$BLUE Running ParamSpider... $NC"
paramspider -d $CLEANED_DOMAIN

# Absolute path to XSStrike
XSStrike_PATH="/home/kali/Desktop/XSStrike"
#Path to save vunerable site and payload
LOG_FILE="results/${CLEANED_DOMAIN}_vulnerable_urls.txt"

# Activate virtual environment for XSStrike
source "${XSStrike_PATH}/xsstrike/bin/activate"

# Read the output file and run XSStrike for each URL
OUTPUT_FILE="results/${CLEANED_DOMAIN}.txt"
if [ -f "$OUTPUT_FILE" ]; then
  while IFS= read -r url; do
    echo -e "$BLUE Running XSStrike on: $url $NC"
    XSStrike_OUTPUT=$(timeout 120 python3 "${XSStrike_PATH}/xsstrike.py" -u "$url" 2>/dev/null)
    
    EXIT_STATUS=$?

    # Check if timeout occurred
    if [ $EXIT_STATUS -eq 124 ]; then
      echo -e "$YELLOW Timeout occurred for URL: $url $NC"
      echo "------------------------------------------------------------------"
      continue
    fi
    
    echo -e "$XSStrike_OUTPUT\n\n"
    echo "----------------------------------------------------------------"
    
    # Check if the output contains a vulnerability indicator
    if echo "$XSStrike_OUTPUT" | grep -q "Payload:*"; then
      # Extract the payload
      PAYLOAD=$(echo "$XSStrike_OUTPUT" | grep "Payload:")
       # Log the vulnerable URL and payload
      echo -e "Vulnerable URL detected: $url\n$PAYLOAD\n" >> "$LOG_FILE"
    else
      continue
    fi
  done < "$OUTPUT_FILE"
else
  echo "Error: Output file not found."
  exit 1
fi

echo "All done!"
