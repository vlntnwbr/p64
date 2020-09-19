# p64 - Python Base64 Decoder ![](https://github.com/vlntnwbr/p64/workflows/Pylint/badge.svg)

This provides a quick entrypoint that decodes a list of base64 string a set
amount of times, displays the result & optionally opens it in Chrome. In order
for the last part to work _chrome.exe_ needs to be accessible via PATH.


## Installation
Installing through [pipx][1] isolates packages in their own environment and exposes their entrypoints via PATH.
```
pipx install https://github.com/vlntnwbr/p64/archive/master.zip
```
Alternatively install regularly via pip: 
```
pip install https://github.com/vlntnwbr/p64/archive/master.zip
```

## Usage
```
# This will decode each string once
PS C:\> p64 SGVsbG8= V29ybGQ=
RESULT    Hello
RESULT    World

# This will decode the string twice and opens the result in chrome
PS C:\> p64 -l 2 -o YUhSMGNITTZMeTluYVhSb2RXSXVZMjl0TDNac2JuUnVkMkp5TDNBMk5BPT0=
OPENING   https://github.com/vlntnwbr/p64

# This will show a detailed help message
PS C:\> p64 -h
usage: p64 [-h] [-l] [-o] base64 [base64 ...]

Decode base64 input n times & optionally open result in chrome.

positional arguments:
  base64         contains list of base64 strings to be decoded

optional arguments:
  -h, --help     show this help message and exit
  -l , --level   defines how many times all input is decoded (default = 1)
  -o, --open     opens all input in chrome if set

p64 will exit if -o, --open is set and chrome can't be located.
```

[1]: https://github.com/pipxproject/pipx