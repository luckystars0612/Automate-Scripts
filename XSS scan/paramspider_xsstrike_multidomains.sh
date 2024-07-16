#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No color
RED='\033[0;31m'

# Check if the correct number of arguments is passed
if [ $# -ne 1 ]; then
    echo "$GREEN Usage: $0 <file_with_urls> $NC"
    exit 1
fi

# Check if the file exists and is readable
if [ ! -f "$1" ]; then
    echo "$RED Error: File '$1' not found or is not readable. $NC"
    exit 1
fi

# Read each URL from the file and call ./xss_spider.sh for each URL
while IFS= read -r url || [ -n "$url" ]; do
    echo -e "$BLUE Running ParamSpider and XSStrike on $url $NC"
    ./xss_spider.sh "$url"
done < "$1"

exit 0
