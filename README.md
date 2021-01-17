# MetExt : Metadata Extractor

MetExt is a Python library and CLI utility that allows to process data in different formats and extract metadata patterns of interest.

## Installation

MetExt requires Python v3.5+.

You need to clone the repository at the moment.

```
$ pip install -r requirements.txt
```

## Usage

### API

### CLI

### Help

```
usage: cli.py [-h] [-i INPUT] [-f FILE] [-r] [-o OUTPUT]
              [-d [{ascii85,base32,base32hex,base58btc,base58ripple,base64,base64url,base85,hex,_id} [{ascii85,base32,base32hex,base58btc,base58ripple,base64,base64url,base85,hex,_id} ...]]]
              [-e [{base32,base64,btc,email,hex,ipv4,ipv6,md5,uri,url,data_uri} [{base32,base64,btc,email,hex,ipv4,ipv6,md5,uri,url,data_uri} ...]]]
              [-F {csv,json,text}] [--per-line]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        File path to process. Wildcards can be used. Reads
                        from STDIN if no input files defined via arguments -i
                        or -f. If -f argument is used, the input file paths
                        are extended with the list of paths from the file.
                        (default: None)
  -f FILE, --file FILE  Read input file paths from a file. One file path per
                        line. (default: None)
  -r, --recursive       Enables recursive wildcards (**) for -i and -f
                        arguments. (default: False)
  -o OUTPUT, --output OUTPUT
                        File to write the output to. Outputs to STDOUT if no
                        file given. (default: ['-'])
  -d [{ascii85,base32,base32hex,base58btc,base58ripple,base64,base64url,base85,hex,_id} [{ascii85,base32,base32hex,base58btc,base58ripple,base64,base64url,base85,hex,_id} ...]], --decode [{ascii85,base32,base32hex,base58btc,base58ripple,base64,base64url,base85,hex,_id} [{ascii85,base32,base32hex,base58btc,base58ripple,base64,base64url,base85,hex,_id} ...]]
                        Select formats that should be tried for decoding from.
                        If no format selected, all will be tried. (default:
                        ['ascii85', 'base32', 'base32hex', 'base58btc',
                        'base58ripple', 'base64', 'base64url', 'base85',
                        'hex'])
  -e [{base32,base64,btc,email,hex,ipv4,ipv6,md5,uri,url,data_uri} [{base32,base64,btc,email,hex,ipv4,ipv6,md5,uri,url,data_uri} ...]], --extract [{base32,base64,btc,email,hex,ipv4,ipv6,md5,uri,url,data_uri} [{base32,base64,btc,email,hex,ipv4,ipv6,md5,uri,url,data_uri} ...]]
                        Select patterns that should be extracted. If no
                        pattern selected, all supported patterns will be
                        tried. (default: ['base32', 'base64', 'btc', 'email',
                        'hex', 'ipv4', 'ipv6', 'md5', 'uri', 'url',
                        'data_uri'])
  -F {csv,json,text}, --out-format {csv,json,text}
                        Select output format of found patterns. (default:
                        ['json'])
  --per-line            Read and process input files per line. Otherwise, read
                        and process all data in each file at once. (default:
                        False)

```

## Currently supported patterns

1. Base32 encoded string
2. Base64 encoded string
3. Bitcoin address
4. E-mail address
5. Hexadecimal data
6. IPv4, IPv6 address
7. MD5 hash string
8. URI, URL

## Tests

Tests are written with pytest.

```
$ pytest
```
