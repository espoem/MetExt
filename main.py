import fileinput
import sys

from Detector.codecs.base64 import Base64
from Detector.extractors.bitcoin_address import BitcoinAddress


def print_help():
    print("python main.py <base64_file> [...base64_file]")


if __name__ == "__main__":
    addresses_found = []
    btc = BitcoinAddress()
    base64 = Base64()
    try:
        with fileinput.input(sys.argv[1:], mode="rb") as f:
            for line in f:
                line_base64_decoded = base64.decode(line)
                if line_base64_decoded:
                    addresses_found += btc.extract_from(
                        line_base64_decoded.decode("ascii")
                    )
    except Exception:
        print_help()
        sys.exit(1)

    if addresses_found:
        print("BTC addresses:")
        print("\n".join(addresses_found))
    else:
        print("No BTC address found")
