import re

from metext.utils.uri import URI, URI_reference, addr_spec

RE_MD5 = re.compile(
    r"\b(?!^[\d]*$)(?!^[a-fA-F]*$)([a-f\d]{32}|[A-F\d]{32})\b"
)  # https://stackoverflow.com/a/25231922
RE_SHA1 = re.compile(r"\b[a-f0-9]{40}\b", re.IGNORECASE)
RE_SHA224 = re.compile(r"\b[a-f0-9]{56}\b", re.IGNORECASE)
RE_SHA256 = re.compile(r"\b[a-f0-9]{64}\b", re.IGNORECASE)
RE_SHA384 = re.compile(r"\b[a-f0-9]{96}\b", re.IGNORECASE)
RE_SHA512 = re.compile(r"\b[a-f0-9]{128}\b", re.IGNORECASE)

RE_URI_REFERENCE = re.compile(r"\b{}\b".format(URI_reference), re.VERBOSE)
RE_URI = re.compile(r"\b{}\b".format(URI), re.VERBOSE)
RE_EMAIL = re.compile(addr_spec, re.VERBOSE)

# https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s13.html
RE_ISBN10 = re.compile(
    r"""
#(?:ISBN(?:-10)?:?\ ?)?     # Optional ISBN/ISBN-10 identifier.
(?=                       # Basic format pre-checks (lookahead):
  [0-9X]{10}             #   Require 10 digits/Xs (no separators).
 |                        #  Or:
  (?=(?:[0-9]+[-\ ]){3})  #   Require 3 separators
  [-\ 0-9X]{13}          #     out of 13 characters total.
)                         # End format pre-checks.
[0-9]{1,5}[-\ ]?          # 1-5 digit group identifier.
[0-9]+[-\ ]?[0-9]+[-\ ]?  # Publisher and title identifiers.
[0-9X]                    # Check digit.
""",
    re.VERBOSE | re.IGNORECASE,
)
RE_ISBN13 = re.compile(
    r"""
#(?:ISBN(?:-13)?:?\ ?)?     # Optional ISBN/ISBN-13 identifier.
(?=                       # Basic format pre-checks (lookahead):
  [0-9]{13}\b              #   Require 13 digits (no separators).
 |                        #  Or:
  (?=(?:[0-9]+[-\ ]){4})  #   Require 4 separators
  [-\ 0-9]{17}\b           #     out of 17 characters total.
)                         # End format pre-checks.
97[89][-\ ]?              # ISBN-13 prefix.
[0-9]{1,5}[-\ ]?          # 1-5 digit group identifier.
[0-9]+[-\ ]?[0-9]+[-\ ]?  # Publisher and title identifiers.
[0-9]                     # Check digit.
""",
    re.VERBOSE | re.IGNORECASE,
)
RE_ISBN = re.compile(
    r"""
#(?:ISBN(?:-1[03])?:?\ ?)?  # Optional ISBN/ISBN-10/ISBN-13 identifier.
(?=                       # Basic format pre-checks (lookahead):
  [0-9X]{10}\b             #   Require 10 digits/Xs (no separators).
 |                        #  Or:
  (?=(?:[0-9]+[-\ ]){3})  #   Require 3 separators
  [-\ 0-9X]{13}\b          #     out of 13 characters total.
 |                        #  Or:
  97[89][0-9]{10}\b        #   978/979 plus 10 digits (13 total).
 |                        #  Or:
  (?=(?:[0-9]+[-\ ]){4})  #   Require 4 separators
  [-\ 0-9]{17}\b           #     out of 17 characters total.
)                         # End format pre-checks.
(?:97[89][-\ ]?)?         # Optional ISBN-13 prefix.
[0-9]{1,5}[-\ ]?          # 1-5 digit group identifier.
[0-9]+[-\ ]?[0-9]+[-\ ]?  # Publisher and title identifiers.
[0-9X]                    # Check digit.
""",
    re.VERBOSE | re.IGNORECASE,
)

RE_ISSN = re.compile(r"\b[0-9]{4}-[0-9]{3}[0-9xX]\b")

RE_DOI = re.compile(r"\b10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])\S)+\b")

RE_BASE32 = re.compile(
    r"(?:[A-Z2-7]{8})*(?:[A-Z2-7]{2}={6}|[A-Z2-7]{4}={4}|[A-Z2-7]{5}={3}|[A-Z2-7]{7}=)?"
)  # https://stackoverflow.com/a/27362880
RE_BASE64 = re.compile(
    r"\b(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/][AQgw]==|[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=)?"
)  # https://www.rise4fun.com/Bek/tutorial/base64

PATTERN_BTC_BASE58 = r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,42}\b"
PATTERN_BTC_SEGWIT = r"\b(?:[bB][cC])1[a-zA-HJ-NP-Z0-9]{25,39}\b"
PATTERN_BCH = (
    r"\b(?:(?:bitcoincash:)?[qp][a-z0-9]{41}|(?:BITCOINCASH:)?[QP][A-Z0-9]{41})\b"
)
PATTERN_ETH = r"\b0x[0-9a-f]{40,42}\b"
PATTERN_ADA_V1 = r"\b(?:Ddz[0-9a-zA-Z]{80,120}|Ae2tdPwUPE[0-9a-zA-Z]{46,53})\b"
PATTERN_ADA_SHELLEY = (
    r"\b(?:addr[0-9a-zA-Z]{99}|stake[0-9a-zA-Z]{54}|[0-9a-zA-Z]{99})\b"
)

RE_BTC = re.compile("{}|{}".format(PATTERN_BTC_SEGWIT, PATTERN_BTC_BASE58))
RE_BTC_WIF = re.compile(
    r"\b(?:[59][a-km-zA-HJ-NP-Z1-9]{50}|[LKc][a-km-zA-HJ-NP-Z1-9]{51})\b"
)
RE_BTC_PRIVKEY = re.compile(r"\b[0-9a-fA-f]{64}\b")
RE_LTC = re.compile(r"\b[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}\b")
RE_XRP = re.compile(r"\br[0-9a-zA-Z]{24,34}\b")
RE_ETH = re.compile(PATTERN_ETH, re.IGNORECASE)
RE_USDT = re.compile(r"{}|{}".format(PATTERN_BTC_BASE58, PATTERN_ETH), re.IGNORECASE)
RE_LINK = RE_ETH
RE_BCH = re.compile(PATTERN_BCH)
RE_BCH_WITH_LEGACY = re.compile(r"{}|{}".format(PATTERN_BTC_BASE58, PATTERN_BCH))
RE_ADA = re.compile(r"{}|{}".format(PATTERN_ADA_V1, PATTERN_ADA_SHELLEY))  # Cardano
RE_DOT = re.compile(r"\b1[a-zA-Z1-9]{25,60}\b")  # Polkadot

RE_PEM = re.compile(
    r"(?:-----BEGIN (?P<label>.+?)-----).+?(?:-----END (?P=label)-----)", re.DOTALL
)
