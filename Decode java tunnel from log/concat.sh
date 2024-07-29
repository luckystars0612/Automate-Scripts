#!/bin/sh

content1=$(cat log20241.tmp)
content2=$(cat log20242.tmp)
content="${content1}${content2}" 
echo "$content" > portal.jsp