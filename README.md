# p64 - Python Base64 Decoder ![](https://github.com/vlntnwbr/p64/workflows/Pylint/badge.svg)

This provides a quick entrypoint that decodes a list of base64 string a set
amount of times, displays the result & optionally opens it in Chrome. In order
for the last part to work _chrome.exe_ needs to be accessible via PATH.


## Installation
Installing through [pipx][1] isolates packages in their own environment and
exposes their entrypoints via PATH.
```
pipx install https://github.com/vlntnwbr/p64/archive/master.zip
```
Alternatively install regularly via pip: 
```
pip install https://github.com/vlntnwbr/p64/archive/master.zip
```

## Usage
```
# Decode each string and open the result in chrome 

PS C:\> p64 aHR0cHM6Ly9naXRodWIuY29tL3ZsbnRud2Jy aHR0cHM6Ly9naXRodWIuY29tL3ZsbnRud2JyL3A2NA==
OPENING   https://github.com/vlntnwbr
OPENING   https://github.com/vlntnwbr/p64
```

### Decode the string twice and print result

```
PS C:\> p64 -s -l 2 U0dWc2JHOGdWMjl5YkdRaA==
RESULT    Hello World!
```
### Show help
```
PS C:\> p64 -h
usage: p64 [-h] [-s] [-l] [-b] base64 [base64 ...]

Decodes base64 input and opens result in given browser. If browser is not specified p64 will use path in 'P64_BROWSER' environment variable.

positional arguments:
  base64           contains list of base64 strings to be decoded

optional arguments:
  -h, --help       show this help message and exit
  -s, --silent     skips opening results in browser if set
  -l , --level     defines how many times all input is decoded (default = 1)
  -b , --browser   path to browser executable.

The application will exit if --silent isn't set and a browser either isn't specified or it'S executable can't be located.
```

[1]: https://github.com/pipxproject/pipx