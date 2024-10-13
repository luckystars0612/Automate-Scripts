# Recover window defender quarantines file
- Sometimes, Window defender will encrypt malicious file into non-executable format using hardcode RC4 key found in mpengine.dll ([Reference](https://jon.glass/blog/quarantines-junk/))
- The **decrypt.py** will take a binary, decode it, and save to new file
- This is a ctf challange in [Huntress ctf](https://huntress.ctf.games/challenges) named **X-ray**. x-ray -> x_ray
- After decrypting, use foremost to extract pe file from binary, all files are in output/ directory.
- Reverse and get the flag
