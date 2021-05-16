# MetExt : Metadata Extractor

MetExt (Metadata Extractor) is a Python library and CLI utility that allows to process data in different formats and extract data patterns of interest.

## Installation

MetExt requires Python v3.5+.

You can install MetExt from PyPi.

```
$ python -m pip install metext
```

Or you can clone the repository install the project locally.

```
$ git clone https://github.com/espoem/MetExt.git
$ cd MetExt
$ python -m pip install -e .
```

Dependencies can also be installed from the `requirements.txt` file.

```
$ python -m pip install -r requirements.txt
```

## CLI

### Help

```
metext --help
```

### Usage

```
metext [-h] [-i INPUT] [-f FILE] [-r] [-o OUTPUT]
        [-d [{quopri,yenc,base58ripple,base64url,pem,base58btc,base85,hexdump,base91,binhex,percent,ascii85,base64,mime,base32,hex,z85,raw,base32crockford,gzip,uu,base32hex} [{quopri,yenc,base58ripple,base64url,pem,base58btc,base85,hexdump,base91,binhex,percent,
  ascii85,base64,mime,base32,hex,z85,raw,base32crockford,gzip,uu,base32hex} ...]]]
        [-e [{bch,xrp,sha256,bip32-xkey,url,ipv4,pem,sha512,ltc,email,chainlink,md5,uuid,btc-wif,sha1,urn,issn,eth,isbn,json,base64,ada,usdt,base32,doi,magnet,sha224,ipv6,uri,data_uri,btc,mac,dot,sha384} [{bch,xrp,sha256,bip32-xkey,url,ipv4,pem,sha512,ltc,email,
  chainlink,md5,uuid,btc-wif,sha1,urn,issn,eth,isbn,json,base64,ada,usdt,base32,doi,magnet,sha224,ipv6,uri,data_uri,btc,mac,dot,sha384} ...]]]
        [-F {text,csv,json}] [--version]
```

Input paths support wildcards. If no input is provided, standard input is processed, i.e. input can be piped into metext. MetExt process input data in best effort, i.e. it tries to decode the data if encoded. The range of decoding to consider can be set via the argument `-d`. The list of patterns to search for is set with the argument `-e`. If not set, all patterns are searched for.

If no decoding is wanted to apply, set `-d raw`.

## API

### List supported modules

```python
from metext import list_decoders_names, list_extractors_names, list_printers_names

if __name__ == "__main__":
    print(list_decoders_names())
    print(list_extractors_names())
    print(list_printers_names())
```

### Analyse data for patterns

```python
from metext import analyse, print_analysis_output

if __name__ == "__main__":
    # file-like object
    with open("filepath", "rb") as fp:
        result = analyse(fp, "raw")  # without decoding, find all supported patterns
        print(result)
        print_analysis_output(result)  # by default prints to STDOUT in JSON format
        print_analysis_output(
            result, "output_filepath", "csv"
        )  # prints to "output_filepath" in CSV format

    # input is list of filepaths
    # consider either no, or base64 encoding
    # extract ipv4 patterns
    result = analyse(["filepath"], ["raw", "base64"], "ipv4")

    # input is string
    # limit decoding to provided decoders with custom kwargs
    # limit patterns to extractors with custom kwargs
    input_data = "some string"
    result = analyse(
        input_data,
        [
            (
                "base64",
                {
                    "charset": "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"
                },
            )
        ],
        [("base64", {})],
    )

    # input is bytes
    # decode data in best effort
    # extract all patterns
    input_data = "some byte string"
    result = analyse(input_data)
```

## Modules

The tool's functionality is divided into individual modules (plugins) of a particular type. A new module can be created by inheriting from one of plugins' bases in [plugin_base.py](https://github.com/espoem/MetExt/blob/master/metext/plugin_base.py) file. A plugin must have defined a unique pair PLUGIN_TYPE, PLUGIN_NAME.

### Supported decoders

| Decoder         | Description                                                |
| --------------- | ---------------------------------------------------------- |
| hex             | Hexadecimal values, optionally with delimiters or prefixes |
| hexdump         | Hexdump format produced by tools `hexdump` and `xdd`       |
| base32          | _base32_ encoding as defined in RFC 4648                   |
| base32hex       | _base32hex_ encoding as defined in RFC 4648                |
| base32crockford | Crockford's Base 32 encoding                               |
| base58btc       | Base 58 encoding using Bitcoin alphabet                    |
| base58ripple    | Base 58 encoding using Ripple alphabet                     |
| base64          | _base64_ encoding as defined in RFC 4648.                  |
| base64url       | _base64url_ encoding as defined in RFC 4648                |
| base85          | _base85_ encoding as defined in RFC 1924                   |
| ascii85         | Ascii85 encoding                                           |
| z85             | Z85 encoding                                               |
| base91          | Base 91 encoding                                           |
| binhex          | BinHex 4.0 encoding                                        |
| pem             | Decodes Base 64 data in PEM format                         |
| gzip            | Decompress GZIP data                                       |
| mime            | Decodes MIME message body                                  |
| percent         | URL-encoding as defined in RFC 3986                        |
| quopri          | Quoted-printable encoding as defined in RFC 2045           |
| uu              | UUEncoding                                                 |
| yenc            | yEnc encoding                                              |

### Supported pattern extractors

| Extractor | Description                                          |
| --------- | ---------------------------------------------------- |
| base32    | _base32_-encoded data                                |
| base64    | _base64_-encoded data                                |
| btc       | Bitcoin P2PKH, P2SH and Bech32 mainnet addresses     |
| btc-wif   | Bitcoin private key in wallet import format (WIF)    |
| bip32-key | Extended private and public keys as defined in BIP32 |
| eth       | Ethereum address                                     |
| ltc       | Litecoin legacy and Bech32 address                   |
| xrp       | XRP (Ripple) classic address                         |
| usdt      | Tether (Omni, Ethereum) address                      |
| bch       | Bitcoin Cash legacy and CashAddr address             |
| chainlink | Chainlink (Ethereum) address                         |
| ada       | Cardano address                                      |
| dot       | Polkadot address                                     |
| email     | E-mail address                                       |
| uuid      | Universally unique identifier (UUID, GUID)           |
| md5       | MD5 hex digest                                       |
| sha1      | SHA-1 hex digest                                     |
| sha224    | SHA-224 hex digest                                   |
| sha256    | SHA-256 hex digest                                   |
| sha384    | SHA-384 hex digest                                   |
| sha512    | SHA-512 hex digest                                   |
| ipv4      | IPv4 address                                         |
| ipv6      | IPv6 address                                         |
| isbn      | ISBN identifier                                      |
| issn      | ISSN identifier                                      |
| doi       | DOI identifier                                       |
| json      | JSON non-empty object or array                       |
| mac       | MAC address                                          |
| pem       | Data in PEM format                                   |
| uri       | Generic URI with a registered scheme                 |
| url       | URL with http(s) or ftp scheme                       |
| urn       | URN                                                  |
| data_uri  | Data URI                                             |
| magnet    | BitTorrent magnet link                               |
