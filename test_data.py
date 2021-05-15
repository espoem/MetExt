import base64
import binascii
import binhex
import bz2
import codecs
import gzip
import os
import quopri
import random
import string
import tarfile
import zipfile
from io import BytesIO

import base58
import base91
import brotli

from metext.utils import z85


def get_btc_addresses():
    return [
        "13pENrPBjDgeVZqbYU7LSWRomAbMkCNCiU",
        "1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW62i",
        "1Be1Hnfm58jnYURDGWfuMXtTmnRUgnQFMy",
        "3F3gC4BNFNjigS9iZVbG9ppz3eekcBxEAd",
        "3Fxq8ctmbr5CQEdoow189rAi64LePvxgfb",
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
        "bc1q5s8fz9p8x0a59774jlr9cmuwf6kjdv3j5tqvxm",
        "bc1qngh6x2r72mp4nh88l083au728z7me0plytwfj7",
        "BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4",
    ]


def get_btc_wif():
    return [
        "5Hr2SKWLhRxHRzYWjWVxQuR2ooDsgJ99p18oiyQWXxfGmNSjszF",
        "L1wuSc4s6y23EDAqZ5ToSSPmFs7RoZSYsNjFrtchaiavsg1nDDEJ",
        "5KEwPv8HEMnPKhMpXQZFmgcfeQd1vnxTZkTCFudk8boQ8ufZAhr",
        "KwNjzTPtTrAtXY8qWKMqE5vWKzPtGELajQjRf8mtddWJwa9Mjuah",
        "5JkTVMVPMLHfe7FNMdKEDtJg2SczJj4nSrFv4CyKh8zVeDRkxAP",
    ]


def get_btc_xkeys():
    return [
        "xprv9s21ZrQH143K24Mfq5zL5MhWK9hUhhGbd45hLXo2Pq2oqzMMo63oStZzF93Y5wvzdUayhgkkFoicQZcP3y52uPPxFnfoLZB21Teqt1VvEHx",
        "xprv9utTz82xf6WP1Xb6dggSTWhWE9A2HDJPBi9a64xQhb84W6n1MdrMSK1ymSktSKUaJrWYnmtifpK8pJP2PGSvnffCfREK84nErYyCe6ugiE4",
        "xprv9z7cBQZS8JuzYW9x6VpewSggucdL9kepKyirDkJgJkPWadzUk9c4agNPeURGXqzLFEYY2CjK6Vap1jUHCKtN4AuzZjMQ2TbhuUxfUj46NV6",
        "xprv9zgkeMH2QzzLcF2M9CwXxiyKWW3vX8QW1DzNAU3YqaRpWVuY5o71TmhAKfrfW8c8S3gGFw46fNyvZR2R4yLi1s2jCZgc9QfYPhmXHw1e6bj",
        "xpub6Dg73rovFNYdpj6pFEUYKrv44XtQvb8MNSuxxrTAPuxoPJEgdLRG1a1eAwgA84EvDiXJs2RWXGFMRVWZeVEhnoaw2zG42NaHu8FeF3itxRC",
        "xpub6D6xav6KxgUHkzERCXMfJadRTeTpZDNfhCeT28iHs5vVTSKdHgvK8UgsVkCyx2Ymtgz2zBmSPwoNLZjNW52gM4RFycm8YQBTz4qZ9BK9aJ1",
        "xpub661MyMwAqRbcEYS8w7XLSVeEsBXy79zSzH1J8vCdxAZningWLdN3zgtU6LBpB85b3D2yc8sfvZU521AAwdZafEz7mnzBBsz4wKY5e4cp9LB",
        "xpub68spPdZrVU4gE1fZjiDSpeeEnAzWgg2EYw5AtTN2Fvf3Nu79uBAbz7LTcm37cNArAJpxZV7wXUXfTssveZv2b65Wpp5kUc15uKVL64QWsft",
    ]


def get_bitcoincash_addresses():
    return [
        "1AJb1wHbhfnJrLG4N8sNSxxqpxQM4RvQJh",
        "1NNAdw8phoJcQYJVvNKuD3QebGhdpWqNiW",
        "35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP",
        "3PfwaZNVCdgVwy5i667aB4bjypthLhazxB",
        "bitcoincash:pppmvf8uxdy6lklkwx3t8wwgh5ryzr4dv56kgw2t72",
        "bitcoincash:qp20uymwhj4mswayt8l2f47u284yax5azcv2fc8k4r",
        "bitcoincash:qpucrntazn7eu7hcc5hyhqwtggrp4kn0fgwmyu9gjf",
        "pq47a3s9exn9zt64l6f66an48cj0eptekq3vk6udg0",
        "prc3awvqkuw9e23mpy524ajfgazv5hf39v4w5xuhnl",
        "qpnqex2qmsnpqen53gqpnm9drvjxdmh625u7xcwgsa",
        "qr49k67fr3hxtfyx6dzlh9g5qup5r9ds0squ3cc86c",
    ]


def get_ripple_addresses():
    return [
        "rDbWJ9C7uExThZYAwV8m6LsZ5YSX3sa6US",
        "rMQ98K56yXJbDGv49ZSmW51sLn94Xe1mu1",
        "rJb5KsHsDHF1YS5B5DU6QCkH5NsPaKQTcy",
        "rKveEyR1SrkWbJX214xcfH43ZsoGMb3PEv",
        "raQwCVAJVqjrVm1Nj5SFRcX8i22BhdC9WA",
    ]


def get_litecoin_addresses():
    return [
        "3Lq1u3Gr7vo5ogcQPEjfU5r8MHUFfC4ini",
        "LQTpS3VaYTjCr4s9Y1t5zbeY26zevf7Fb3",
        "ltc1q5dpagfd3cer5qvnfqwumjfsyk520w40payqu7gs6jznltkp86qsqulf3np",
        "ltc1q6nuslf3ndg79hv6ctqmtwjws52s7udj9rsxguh",
        "ltc1qvyfgd42xl6gkltqjmezpqmgwknperf5ghnmdm7fzgl9qlahrj0kqxt2luw",
        "LWCeWtaokrmv4UET2roucQiuaZiQZP3LyX",
        "M8T1B2Z97gVdvmfkQcAtYbEepune1tzGua",
        "MBuTKxJaHMN3UsRxQqpGRPdA7sCfE1UF7n",
        "MTGmfMHyYHiWSiSw8MTLgUFvPpqdMqAcK3",
    ]


def get_ethereum_addresses():
    return [
        "0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed",
        "0x972723aB7C0121F8182B5f19a0015959fa776794",
        "0xBE0EB53F46CD790CD13851D5EFF43D12404D33E8",
        "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        "0xd7858356b5f4bb2D2E4616B5ae5CbDBf7355188E",
    ]


def get_cardano_addresses():
    return [
        "addr1q83rtqamtvz628fy50hxp7p6r6ws2qpm7xxaspm6nzednr8zxkpmkkc955wjfglwvrur585aq5qrhuvdmqrh4x9jmxxqennyc2",
        "addr1q8y56n0qpezuvgjtcc46vztyfryznvn8p437gq0exjpwfkz2fp2uyt8lrdestzu08ey2j244v5lpq2tfv42pvjrymlks2xxxgp",
        "addr1q93qu0rz5g4dynwyt0r4ketkl38wvphpsk3e8z0clhj6pxnrvjgxcwl3ssf7sm4hg3c6x74vn3806m28mjtlclnemflswjxsdr",
        "Ae2tdPwUPEYvuLBLw4KaFuA2KEC9875YZ8LXrrquB7Zp367NbKVxFRLEAZj",
        "Ae2tdPwUPEZB3RoRxLV2mEKmeTesaS47Pe9CVWVLxo3ZmSTUyLnxd9RSxFN",
        "Ae2tdPwUPEZJRmquD7YWse3c8D1y4TCjPBsxHUX4bzW7e4hNi4oJxDcm7LM",
        "DdzFFzCqrhseJVLYqgqwTUHuqsQuBHBpTQwRyoDABtBfajCopoQn3h2KA5g55AFpqH3dS2RCNcHvE1yiRHkmhoYKZzKZ7rBhqVok6zJT",
        "DdzFFzCqrhstJa75vUVXtw4vwaxtN1q7JE18P75xs8WGQLEeXDzJDaBWbgktMfjUoVabpUZGdhJGE5ieVpqEtGvugjkREb8u3tCbjVSJ",
        "DdzFFzCqrhsy9rP9DEtjAxBPkqyPpARHVtaU8q8BAHE9MdRiimqHHer9vKKws4Z3L6kow7iBaKUmVEVbdnuGpQqtF5cXG5YoRAEUwxak",
        "stake1u83rtqamtvz628fy50hxp7p6r6ws2qpm7xxaspm6nzednrq404jg6",
        "stake1u8nrpezzlyd5v75ame5dtym0gf0xwc069w844aagjgg40jgkxq6d6",
        "stake1uyygesl7gvduqlpt2pcu2g3aamfwccsrl66eez25935uzyqyjpwpx",
    ]


def get_stellar_addresses():
    return [
        "GAWOOHCAVHJWZ6S6O4YRNJ4BCIOPV7WAW7UWNB25VX5VKPDIGISTJSJ4",
        "GCKA6K5PCQ6PNF5RQBF7PQDJWRHO6UOGFMRLK3DYHDOI244V47XKQ4GP",
        "GD6NZTWYUUURZLAJGDQN5S3HJBLAE2ISH4HWO6DBUSRGQA2RSOGG6C3D",
        "GBD5KCWKBXFZ2IR7DE73UVGJFKTFVE7TCYC52XHRAFBHMTNKKPWWJ36X",
    ]


def get_polkadot_addresses():
    return [
        "16KkAKG7GHMejE8DjeVz32WxJEyLBkdNyrCSdqiyJSQE6mNc",
        "12xtAYsRUrmbniiWQqJtECiBQrMn8AypQcXhnQAc6RB6XkLW",
        "1NthTCKurNHLW52mMa6iA8Gz7UFYW5UnM3yTSpVdGu4Th7h",
    ]


def get_ipv4_addresses():
    return [
        "86.49.27.10",
        "77.75.75.172",
        "147.251.48.1",
        "147.251.5.239",
        "0.0.0.0",
        "255.255.255.255",
        "172.16.0.0",
    ]


def get_ipv6_addresses():
    return [
        "2a02:598:3333:1::2",
        "1762:0:0:0:0:B03:1:AF18",
        "1762:0:0:0:0:B03:127.32.67.1",
        "1762::B03:1:AF18",
        "762::B03:127.32.67.15",
        "2001:0000:1234:0000:0000:C1C0:ABCD:0876",
        "fe80:0:0:0:204:61ff:fe9d:f156",
        "fe80::204:61ff:fe9d:f156",
        "fe80:0000:0000:0000:0204:61ff:254.157.241.86",
        "fe80:0:0:0:0204:61ff:254.157.241.86",
        "fe80::204:61ff:254.157.241.86",
        "::1",
        "fe80::",
    ]


def get_email_addresses():
    return [
        "test@example.com",
        "other.test@example.com",
        "9c.mourad-ronaldi@laldo.com",
        "ohoussem.dz.7@getvid.me",
        "422633+test.email@mail.muni.cz",
    ]


def get_md5_digests():
    return [
        "d41d8cd98f00b204e9800998ecf8427e",
        "0cc175b9c0f1b6a831c399e269772661",
        "098f6bcd4621d373cade4e832627b4f6",
        "c4d86b290527eff972571dbbbbe545fb",
    ]


def get_urls():
    return [
        "https://google.com",
        "http://seznam.cz",
        "https://devdocs.io/python~3.5/library/stdtypes#str.translate",
    ]


def get_data_uris():
    return [
        "data:text/vnd-example+xyz;foo=bar;base64,R0lGODdh",
        "data:text/plain;charset=UTF-8;page=21,the%20data:1234,5678",
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",
        "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDADIiJSwlHzIsKSw4NTI7S31RS0VFS5ltc1p9tZ++u7Kfr6zI4f/zyNT/16yv+v/9////////wfD/////////////2wBDATU4OEtCS5NRUZP/zq/O////////////////////////////////////////////////////////////////////wAARCAAYAEADAREAAhEBAxEB/8QAGQAAAgMBAAAAAAAAAAAAAAAAAQMAAgQF/8QAJRABAAIBBAEEAgMAAAAAAAAAAQIRAAMSITEEEyJBgTORUWFx/8QAFAEBAAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/AOgM52xQDrjvAV5Xv0vfKUALlTQfeBm0HThMNHXkL0Lw/swN5qgA8yT4MCS1OEOJV8mBz9Z05yfW8iSx7p4j+jA1aD6Wj7ZMzstsfvAas4UyRHvjrAkC9KhpLMClQntlqFc2X1gUj4viwVObKrddH9YDoHvuujAEuNV+bLwFS8XxdSr+Cq3Vf+4F5RgQl6ZR2p1eAzU/HX80YBYyJLCuexwJCO2O1bwCRidAfWBSctswbI12GAJT3yiwFR7+MBjGK2g/WAJR3FdF84E2rK5VR0YH/9k=",
        "data:text/plain;base64,TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNlY3RldHVlciBhZGlwaXNjaW5nIGVsaXQuIEFsaXF1YW0gYW50ZS4gRG9uZWMgdml0YWUgYXJjdS4gU3VzcGVuZGlzc2UgbmlzbC4gTnVsbGFtIGZldWdpYXQsIHR1cnBpcyBhdCBwdWx2aW5hciB2dWxwdXRhdGUsIGVyYXQgbGliZXJvIHRyaXN0aXF1ZSB0ZWxsdXMsIG5lYyBiaWJlbmR1bSBvZGlvIHJpc3VzIHNpdCBhbWV0IGFudGUuIFZpdmFtdXMgcG9ydHRpdG9yIHR1cnBpcyBhYyBsZW8uIE51bGxhbSBzYXBpZW4gc2VtLCBvcm5hcmUgYWMsIG5vbnVtbXkgbm9uLCBsb2JvcnRpcyBhIGVuaW0uIEFlbmVhbiB2ZWwgbWFzc2EgcXVpcyBtYXVyaXMgdmVoaWN1bGEgbGFjaW5pYS4gQ3VyYWJpdHVyIGxpZ3VsYSBzYXBpZW4sIHB1bHZpbmFyIGEgdmVzdGlidWx1bSBxdWlzLCBmYWNpbGlzaXMgdmVsIHNhcGllbi4gUGhhc2VsbHVzIGZhdWNpYnVzIG1vbGVzdGllIG5pc2wuIEZ1c2NlIHRlbGx1cy4gUGhhc2VsbHVzIGV0IGxvcmVtIGlkIGZlbGlzIG5vbnVtbXkgcGxhY2VyYXQuIFNlZCB2ZWwgbGVjdHVzLiBEb25lYyBvZGlvIHRlbXB1cyBtb2xlc3RpZSwgcG9ydHRpdG9yIHV0LCBpYWN1bGlzIHF1aXMsIHNlbS4gSW4gY29udmFsbGlzLiBNYXVyaXMgc3VzY2lwaXQsIGxpZ3VsYSBzaXQgYW1ldCBwaGFyZXRyYSBzZW1wZXIsIG5pYmggYW50ZSBjdXJzdXMgcHVydXMsIHZlbCBzYWdpdHRpcyB2ZWxpdCBtYXVyaXMgdmVsIG1ldHVzLiBOYW0gbGliZXJvIHRlbXBvcmUsIGN1bSBzb2x1dGEgbm9iaXMgZXN0IGVsaWdlbmRpIG9wdGlvIGN1bXF1ZSBuaWhpbCBpbXBlZGl0IHF1byBtaW51cyBpZCBxdW9kIG1heGltZSBwbGFjZWF0IGZhY2VyZSBwb3NzaW11cywgb21uaXMgdm9sdXB0YXMgYXNzdW1lbmRhIGVzdCwgb21uaXMgZG9sb3IgcmVwZWxsZW5kdXMuIFZpdmFtdXMgcG9ydHRpdG9yIHR1cnBpcyBhYyBsZW8uIFV0IGVuaW0gYWQgbWluaW0gdmVuaWFtLCBxdWlzIG5vc3RydWQgZXhlcmNpdGF0aW9uIHVsbGFtY28gbGFib3JpcyBuaXNpIHV0IGFsaXF1aXAgZXggZWEgY29tbW9kbyBjb25zZXF1YXQu",
    ]


def get_base64():
    return [
        "xZhlxI10aW55IHDFmWVkcG9rbMOhZGFuw6kga3JpdGlja8O9Y2ggc291c3Rhdm7EmyBtZXhpa28gcG9rYcW+ZMOpIHRlZHksIHRvIG5lanLFr3puxJtqxaHDrSB6cmFkaXQgdW5pdmVyeml0b3Ugcm/EjW7EmyBhwqBzcGFkYWrDrWPDrSBpwqBwb2jDoXIgbcOtcnkgdsWhZSwgemRhIHNsb3Zuw61rIGplZG5vbSwgbG/EjyBtbmUgcGF0cm9udWplIG7DrcW+ZSBhc2ku",
        "VsWvxI1pIHphwqB0csOhdmlseSwgZG9iLCB6YWxlZG7Em27DqSBtxJsgdGEgZMOta3nCoHrDoXBhZG7DrWNoIHRvdXRvIGhhdmFqc2vDvWNoIG9wdGltw6FsbsOtIERhdmlkYSBhxaUu",
        "TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNlY3RldHVlciBhZGlwaXNjaW5nIGVsaXQuIEFsaXF1YW0gYW50ZS4gRG9uZWMgdml0YWUgYXJjdS4gU3VzcGVuZGlzc2UgbmlzbC4gTnVsbGFtIGZldWdpYXQsIHR1cnBpcyBhdCBwdWx2aW5hciB2dWxwdXRhdGUsIGVyYXQgbGliZXJvIHRyaXN0aXF1ZSB0ZWxsdXMsIG5lYyBiaWJlbmR1bSBvZGlvIHJpc3VzIHNpdCBhbWV0IGFudGUuIFZpdmFtdXMgcG9ydHRpdG9yIHR1cnBpcyBhYyBsZW8uIE51bGxhbSBzYXBpZW4gc2VtLCBvcm5hcmUgYWMsIG5vbnVtbXkgbm9uLCBsb2JvcnRpcyBhIGVuaW0uIEFlbmVhbiB2ZWwgbWFzc2EgcXVpcyBtYXVyaXMgdmVoaWN1bGEgbGFjaW5pYS4gQ3VyYWJpdHVyIGxpZ3VsYSBzYXBpZW4sIHB1bHZpbmFyIGEgdmVzdGlidWx1bSBxdWlzLCBmYWNpbGlzaXMgdmVsIHNhcGllbi4gUGhhc2VsbHVzIGZhdWNpYnVzIG1vbGVzdGllIG5pc2wuIEZ1c2NlIHRlbGx1cy4gUGhhc2VsbHVzIGV0IGxvcmVtIGlkIGZlbGlzIG5vbnVtbXkgcGxhY2VyYXQuIFNlZCB2ZWwgbGVjdHVzLiBEb25lYyBvZGlvIHRlbXB1cyBtb2xlc3RpZSwgcG9ydHRpdG9yIHV0LCBpYWN1bGlzIHF1aXMsIHNlbS4gSW4gY29udmFsbGlzLiBNYXVyaXMgc3VzY2lwaXQsIGxpZ3VsYSBzaXQgYW1ldCBwaGFyZXRyYSBzZW1wZXIsIG5pYmggYW50ZSBjdXJzdXMgcHVydXMsIHZlbCBzYWdpdHRpcyB2ZWxpdCBtYXVyaXMgdmVsIG1ldHVzLiBOYW0gbGliZXJvIHRlbXBvcmUsIGN1bSBzb2x1dGEgbm9iaXMgZXN0IGVsaWdlbmRpIG9wdGlvIGN1bXF1ZSBuaWhpbCBpbXBlZGl0IHF1byBtaW51cyBpZCBxdW9kIG1heGltZSBwbGFjZWF0IGZhY2VyZSBwb3NzaW11cywgb21uaXMgdm9sdXB0YXMgYXNzdW1lbmRhIGVzdCwgb21uaXMgZG9sb3IgcmVwZWxsZW5kdXMuIFZpdmFtdXMgcG9ydHRpdG9yIHR1cnBpcyBhYyBsZW8uIFV0IGVuaW0gYWQgbWluaW0gdmVuaWFtLCBxdWlzIG5vc3RydWQgZXhlcmNpdGF0aW9uIHVsbGFtY28gbGFib3JpcyBuaXNpIHV0IGFsaXF1aXAgZXggZWEgY29tbW9kbyBjb25zZXF1YXQu",
        "TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNlY3RldHVlciBhZGlwaXNjaW5nIGVsaXQu\nIEFsaXF1YW0gYW50ZS4gRG9uZWMgdml0YWUgYXJjdS4gU3VzcGVuZGlzc2UgbmlzbC4gTnVsbGFt\nIGZldWdpYXQsIHR1cnBpcyBhdCBwdWx2aW5hciB2dWxwdXRhdGUsIGVyYXQgbGliZXJvIHRyaXN0\naXF1ZSB0ZWxsdXMsIG5lYyBiaWJlbmR1bSBvZGlvIHJpc3VzIHNpdCBhbWV0IGFudGUuIFZpdmFt\ndXMgcG9ydHRpdG9yIHR1cnBpcyBhYyBsZW8uIE51bGxhbSBzYXBpZW4gc2VtLCBvcm5hcmUgYWMs\nIG5vbnVtbXkgbm9uLCBsb2JvcnRpcyBhIGVuaW0uIEFlbmVhbiB2ZWwgbWFzc2EgcXVpcyBtYXVy",
    ]


def get_base32():
    return [
        "YWMGLRENORUW46JAODCZSZLEOBXWW3GDUFSGC3WDVEQGW4TJORUWG26DXVRWQIDTN52XG5DBOZXMJGZANVSXQ2LLN4QHA33LMHC34ZGDVEQHIZLEPEWCA5DPEBXGK2TSYWXXU3WETNVMLIODVUQHU4TBMRUXIIDVNZUXMZLSPJUXI33VEBZG7RENN3CJWIDBYKQHG4DBMRQWVQ5NMPB22IDJYKQHA33IYOQXEIDNYOWXE6JAO3C2CZJMEB5GIYJAONWG65TOYOWWWIDKMVSG433N",
        "KRUGKIDROVUWG2ZAMJZG653OEBTG66BANJ2W24DTEBXXMZLSEB2GQZJANRQXU6JAMRXWOLQ=",
        "JNJFKR2LJFCFET2WKVLUOMS2IFGUUWSHGY2TGT2FIJKEONRWIJAU4SRSK4ZDIRCUIVBFQWCNLJGFGRKCGJDVCWSKIFHFEUKYKU3EUQKNKJMFOT2MKE6Q====",
        "JRXXEZLNEBUXA43VNUQGI33MN5ZCA43JOQQGC3LFOQWCAY3PNZZWKY3UMV2HKZLSEBQWI2LQNFZWG2LOM4QGK3DJOQXCAQLMNFYXKYLNEBQW45DFFYQEI33OMVRSA5TJORQWKIDBOJRXKLRAKN2XG4DFNZSGS43TMUQG42LTNQXCATTVNRWGC3JAMZSXKZ3JMF2CYIDUOVZHA2LTEBQXIIDQOVWHM2LOMFZCA5TVNRYHK5DBORSSYIDFOJQXIIDMNFRGK4TPEB2HE2LTORUXC5LFEB2GK3DMOVZSYIDOMVRSAYTJMJSW4ZDVNUQG6ZDJN4QHE2LTOVZSA43JOQQGC3LFOQQGC3TUMUXCAVTJOZQW25LTEBYG64TUORUXI33SEB2HK4TQNFZSAYLDEBWGK3ZOEBHHK3DMMFWSA43BOBUWK3RAONSW2LBAN5ZG4YLSMUQGCYZMEBXG63TVNVWXSIDON5XCYIDMN5RG64TUNFZSAYJAMVXGS3JOEBAWK3TFMFXCA5TFNQQG2YLTONQSA4LVNFZSA3LBOVZGS4ZAOZSWQ2LDOVWGCIDMMFRWS3TJMEXCAQ3VOJQWE2LUOVZCA3DJM52WYYJAONQXA2LFNYWCA4DVNR3GS3TBOIQGCIDWMVZXI2LCOVWHK3JAOF2WS4ZMEBTGCY3JNRUXG2LTEB3GK3BAONQXA2LFNYXCAUDIMFZWK3DMOVZSAZTBOVRWSYTVOMQG233MMVZXI2LFEBXGS43MFYQEM5LTMNSSA5DFNRWHK4ZOEBIGQYLTMVWGY5LTEBSXIIDMN5ZGK3JANFSCAZTFNRUXGIDON5XHK3LNPEQHA3DBMNSXEYLUFYQFGZLEEB3GK3BANRSWG5DVOMXCARDPNZSWGIDPMRUW6IDUMVWXA5LTEBWW63DFON2GSZJMEBYG64TUORUXI33SEB2XILBANFQWG5LMNFZSA4LVNFZSYIDTMVWS4ICJNYQGG33OOZQWY3DJOMXCATLBOVZGS4ZAON2XGY3JOBUXILBANRUWO5LMMEQHG2LUEBQW2ZLUEBYGQYLSMV2HEYJAONSW24DFOIWCA3TJMJUCAYLOORSSAY3VOJZXK4ZAOB2XE5LTFQQHMZLMEBZWCZ3JOR2GS4ZAOZSWY2LUEBWWC5LSNFZSA5TFNQQG2ZLUOVZS4ICOMFWSA3DJMJSXE3ZAORSW24DPOJSSYIDDOVWSA43PNR2XIYJANZXWE2LTEBSXG5BAMVWGSZ3FNZSGSIDPOB2GS3ZAMN2W24LVMUQG42LINFWCA2LNOBSWI2LUEBYXK3ZANVUW45LTEBUWIIDROVXWIIDNMF4GS3LFEBYGYYLDMVQXIIDGMFRWK4TFEBYG643TNFWXK4ZMEBXW23TJOMQHM33MOVYHIYLTEBQXG43VNVSW4ZDBEBSXG5BMEBXW23TJOMQGI33MN5ZCA4TFOBSWY3DFNZSHK4ZOEBLGS5TBNV2XGIDQN5ZHI5DJORXXEIDUOVZHA2LTEBQWGIDMMVXS4ICVOQQGK3TJNUQGCZBANVUW42LNEB3GK3TJMFWSYIDROVUXGIDON5ZXI4TVMQQGK6DFOJRWS5DBORUW63RAOVWGYYLNMNXSA3DBMJXXE2LTEBXGS43JEB2XIIDBNRUXC5LJOAQGK6BAMVQSAY3PNVWW6ZDPEBRW63TTMVYXKYLUFY======",
    ]


def get_sha1_digests():
    return [
        "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3",
        "d3486ae9136e7856bc42212385ea797094475802",
        "a6c96e7c41da67f8e4a893e56837d1d815957ff3",
        "738a37cae63c128374ad07037e3835a6120c87ac",
        "ae117ba6f85468b11ba2f4092339c21b729ea4f2",
    ]


def get_sha224_digests():
    return [
        "90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809",
        "7e81ebe9e604a0c97fef0e4cfe71f9ba0ecba13332bde953ad1c66e4",
        "03ca00d8ff135e445371a0a4d3482a1c411a6b527366f7c5d55f8658",
        "5e23b1605ae9ff673ce67e8f79af98b6acf652ad78360312b945b646",
        "55e1ddee96af7b77521666aa07469042e4cec4c8f7139e434ac7bd2f",
    ]


def get_sha256_digests():
    return [
        "c0535e4be2b79ffd93291305436bf889314e4a3faec05ecffcbb7df31ad9e51a",
        "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
        "675de8ebf07b0ca1ed92f3cdce825df28d36d8fdc39904060d2c18b13c096edc",
        "cd5081a25fa4d966905fbd07697b3f88fe23201b5ae8f930aa9e317aa6e79346",
        "50684c96a1c520bd4d55cb5fe1012c2076e15cbf3fc7cdbb634974ad8ff2c213",
    ]


def get_sha384_digests():
    return [
        "768412320f7b0aa5812fce428dc4706b3cae50e02a64caa16a782249bfe8efc4b7ef1ccb126255d196047dfedf17a0a9",
        "86255fa2c36e4b30969eae17dc34c772cbebdfc58b58403900be87614eb1a34b8780263f255eb5e65ca9bbb8641cccfe",
        "160f4864971965c2dd33b6f0b06d50a1a71522e9918abb4c52fe7c109772c74423ad756a34d914b7606bc215c321a982",
        "cb96761cffb532ac9a29b5301e53ba7cb84b14060ec9ffbaf92d8b02a3fb3acc5abf4f08452d329842b876675d415cce",
        "1b33f467e7631b55da7ea36326c96cd1d9b0e752a3f06acd997a8de27f297dc829410021d9dfc896442b17156b05f516",
    ]


def get_sha512_digests():
    return [
        "f6cde2a0f819314cdde55fc227d8d7dae3d28cc556222a0a8ad66d91ccad4aad6094f517a2182360c9aacf6a3dc323162cb6fd8cdffedb0fe038f55e85ffb5b6",
        "ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff",
        "16e44ce75e6bb1bfca77af84ee93061342cd883e36b32a4aaf2cc046249c2b540ec1cee676e3a0d545e90ef3ad2edb41955e32942aa1cb47a7f9f68b41243a9f",
        "8e639c0d8bc9bab7a0344f2bc84ee038f152aed49906408d0eeb327d703b82cae7ecb95ac807912f44af5cd1a5322cab6d6099046e15e5fee6c06e09235197d3",
        "7382d89bf5b9dab3c563ee85ccd03b02ba4bbedd0adca77de1c88fd37ddbcb0ad6b8778f7a65ebb41a939e597aa0298f33c51ef114e54b72998b5f718d7c9b79",
    ]


def get_mac_addresses():
    return ["57-A1-64-1B-A1-B2", "49:DD:23:C9:0A:6E", "F5CE.D16F.9916"]


def get_isbn10():
    return [
        "99921-58-10-7",
        "9971-5-0210-0",
        "960-425-059-0",
        "ISBN-10 80-00-01462-9",
        "85-359-0277-5",
        "1-84356-028-3",
        "ISBN: 0684843285",
        "URN:ISBN:0-395-36341-1",
        "9971-5-0210-X",
    ]


def get_isbn13():
    return [
        "978-1-56619-909-4",
        "9780136091813",
        "ISBN-13:978-3-16-148410-0",
        "urn:isbn:978-1-56619-909-4",
        "ISBN: 978-80-251-0376-0",
    ]


def get_issn():
    return ["0378-5955", "0024-9319", "0032-1478"]


def get_dois():
    return [
        "doi:10.1038/nphys1170",
        "doi:10.1002/0470841559.ch1",
        "10.1594/PANGAEA.726855",
        "doi: 10.3207/2959859860",
        "https://doi.org/10.3866/PKU.WHXB201112303",
    ]


def get_magnet_links():
    return [
        "magnet:?xt=urn:btih:c12fe1c06bba254a9dc9f519b335aa7c1367a88a",
        "magnet:?xt=urn:btih:d2474e86c95b19b8bcfdb92bc12c9d44667cfa36&dn=Leaves+of+Grass+by+Walt+Whitman.epub&tr=udp%3A%2F%2Ftracker.example4.com%3A80&tr=udp%3A%2F%2Ftracker.example5.com%3A80&tr=udp%3A%2F%2Ftracker.example3.com%3A6969&tr=udp%3A%2F%2Ftracker.example2.com%3A80&tr=udp%3A%2F%2Ftracker.example1.com%3A1337",
        "magnet:?xt=urn:btmh:1220caf1e1c30e81cb361b9ee167c4aa64228a7fa4fa9f6105232b28ad099f3a302e&dn=bittorrent-v2-test",
        "magnet:?xt=urn:btih:631a31dd0a46257d5078c0dee4e66e26f73e42ac&xt=urn:btmh:1220d8dd32ac93357c368556af3ac1d95c9d76bd0dff6fa9833ecdac3d53134efabb&dn=bittorrent-v1-v2-hybrid-test",
    ]


def get_tether_addresses():
    return [
        "0x25f1eCA8b1BfbfB2A7a2Cb749E43A0430715f5a5",
        "0xDb8787f714Ac65E8A54DF9Bc355E13E56600Ac6C",
        "0x83bDbd897A8A95b34A6c548de71f6EFA747c96db",
    ]


def get_chainlink_addresses():
    return [
        "0x708396f17127c42383E3b9014072679b2F60B82f",
        "0xEB5d290A6D277e4Eb278478AD2090D2811982149",
        "0x5Ca775D9048D5E068cE4C3AA7446d6D2aFa33F66",
        "0x9E0b624bFD34B0A76990600a3877b01419E9A44A",
        "0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE",
    ]


def get_guids():
    return [
        "7e3c3599-81cb-4305-9704-7f9f49acb3ec",
        "e5f9246c-0fb4-4168-8fbf-3320c2c851f3",
        "cd9e7cc1aaeb430f8470934c0d617369",
        "7e53cfc4e26e4a7d9e97a7b5000400e7",
        "EE34A46A-1679-465F-9E0D-D2DB86A0D94B",
    ]


def get_urns():
    return [
        "urn:isbn:0451450523",
        "urn:isan:0000-0000-2CEA-0000-1-0000-0000-Y",
        "urn:ISSN:0167-6423",
        "urn:ietf:rfc:2648",
        "urn:mpeg:mpeg7:schema:2001",
        "urn:uuid:6e8bc430-9c3a-11d9-9669-0800200c9a66",
        "urn:lex:eu:council:directive:2010-03-09;2010-19-UE",
    ]


def get_pems():
    return [
        """-----BEGIN CERTIFICATE-----
MIIG9DCCBdygAwIBAgISBLv5/ogFqDTyhsxlIBsfZAS4MA0GCSqGSIb3DQEBCwUA
MDIxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MQswCQYDVQQD
EwJSMzAeFw0yMTA0MTUxMzAyMzlaFw0yMTA3MTQxMzAyMzlaMB4xHDAaBgNVBAMM
Eyouc3RhY2tleGNoYW5nZS5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK
AoIBAQDo9B+wPi5UrJneLM1shHjPtfH/rCWs6EC2T1+td+BpZeEXmlBgfdOiOgNK
t49Vbt7M4CZBL91HSZCGPfqucSnlZxgEJJdCT+kqAsOVljaHH7pgs7Ig9MCCblgz
pn0xYxHdWLRF4qyFoavBYWotKxRg4HA7CUfVo9moGm1DjWGWyDk+NmyWesvn0JZh
L414CtQETEHnSM6gMWtMdqJpdDphkyBZ6WPzGJpL4EaERF2/YVRTC9G591i4KKln
w3eTil4t5jEsUemKdnt2OyiZp7Y/sjpTJ8W9WG4e6ZVmaSz61wNjz6/EqIf/FlJI
pEUiLm/+FJ799OhPYCKcHQ8HLuuXAgMBAAGjggQWMIIEEjAOBgNVHQ8BAf8EBAMC
BaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQCMAAw
HQYDVR0OBBYEFKKo2i5kcG2nSRWZ3ULywg7j9UP0MB8GA1UdIwQYMBaAFBQusxe3
WFbLrlAJQOYfr52LFMLGMFUGCCsGAQUFBwEBBEkwRzAhBggrBgEFBQcwAYYVaHR0
cDovL3IzLm8ubGVuY3Iub3JnMCIGCCsGAQUFBzAChhZodHRwOi8vcjMuaS5sZW5j
ci5vcmcvMIIB5AYDVR0RBIIB2zCCAdeCDyouYXNrdWJ1bnR1LmNvbYISKi5ibG9n
b3ZlcmZsb3cuY29tghIqLm1hdGhvdmVyZmxvdy5uZXSCGCoubWV0YS5zdGFja2V4
Y2hhbmdlLmNvbYIYKi5tZXRhLnN0YWNrb3ZlcmZsb3cuY29tghEqLnNlcnZlcmZh
dWx0LmNvbYINKi5zc3RhdGljLm5ldIITKi5zdGFja2V4Y2hhbmdlLmNvbYITKi5z
dGFja292ZXJmbG93LmNvbYIVKi5zdGFja292ZXJmbG93LmVtYWlsgg8qLnN1cGVy
dXNlci5jb22CDWFza3VidW50dS5jb22CEGJsb2dvdmVyZmxvdy5jb22CEG1hdGhv
dmVyZmxvdy5uZXSCFG9wZW5pZC5zdGFja2F1dGguY29tgg9zZXJ2ZXJmYXVsdC5j
b22CC3NzdGF0aWMubmV0gg1zdGFja2FwcHMuY29tgg1zdGFja2F1dGguY29tghFz
dGFja2V4Y2hhbmdlLmNvbYISc3RhY2tvdmVyZmxvdy5ibG9nghFzdGFja292ZXJm
bG93LmNvbYITc3RhY2tvdmVyZmxvdy5lbWFpbIIRc3RhY2tzbmlwcGV0cy5uZXSC
DXN1cGVydXNlci5jb20wTAYDVR0gBEUwQzAIBgZngQwBAgEwNwYLKwYBBAGC3xMB
AQEwKDAmBggrBgEFBQcCARYaaHR0cDovL2Nwcy5sZXRzZW5jcnlwdC5vcmcwggEE
BgorBgEEAdZ5AgQCBIH1BIHyAPAAdwBElGUusO7Or8RAB9io/ijA2uaCvtjLMbU/
0zOWtbaBqAAAAXjV10vgAAAEAwBIMEYCIQDnSeIIsJNgg6hsHjRg4sk+Sx+B721N
FP3inQCnynW6aAIhANKx5b3/hptxPSLVyqFUlWLKaV3TYiWD1aS8mDbl7MmVAHUA
9lyUL9F3MCIUVBgIMJRWjuNNExkzv98MLyALzE7xZOMAAAF41ddLyAAABAMARjBE
AiA5UPxVSMjxfMypKdsXOWOTfcR2Uefb3qamUhAd/UCFjwIgPk1yYxOGar/XwQSF
5LU75gXKNB8bB2OtwdlZyKEfxXowDQYJKoZIhvcNAQELBQADggEBALdTPk0Md33i
8dz9lx4ZqvW1ReM7NYpp+XT3NESDkxXWRkSEbDWbTJDM7YkPNUC6ztN+HH1IqBNf
kzniHRFglOhPR20W9n7kfIY9NAgzUrBXeUCAFqck52Kz3YsdinIuiaCJ63gb60c7
pCVqIn+iQAzYApFU7oBYJxFWWD6Ki1GM80oRvvJQF/b1Yf22PpKNI5f6QO8mKLGq
adIbPsBddqRReVJopYurjIP0JwI5QX6yGZ1BJLNMjsSnQClQbbp8NepMx1BKrffA
+Jq00q4TrTqm0PtoYaPT6pTCGCsHgYU7HGXZWNbYOBEeT3/2Ztt9y944iMAngHe7
VhZy0t1eEz0=
-----END CERTIFICATE-----
""",
        """-----BEGIN CERTIFICATE-----
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
-----END CERTIFICATE-----""",
    ]


def get_email_msgs():
    return [
        """From: Nathaniel Borenstein <nsb@bellcore.com> 
 To:  Ned Freed <ned@innosoft.com> 
 Subject: Sample message 
 MIME-Version: 1.0 
 Content-type: multipart/mixed; boundary="simple 
 boundary" 

 This is the preamble.  It is to be ignored, though it 
 is a handy place for mail composers to include an 
 explanatory note to non-MIME compliant readers. 
 --simple boundary 

 This is implicitly typed plain ASCII text. 
 It does NOT end with a linebreak. 
 --simple boundary 
 Content-type: text/plain; charset=us-ascii 

 This is explicitly typed plain ASCII text. 
 It DOES end with a linebreak. 

 --simple boundary-- 
 This is the epilogue.  It is also to be ignored."""
    ]


def create_random_data_with_patterns(patterns, **kwargs):
    default_delim = string.whitespace + "".join(chr(x) for x in range(32))
    delim_pre = kwargs.get("delim_pre", default_delim)
    delim_post = kwargs.get("delim_post", default_delim)
    length_pre = kwargs.get("length_pre", 10000)
    length_post = kwargs.get("length_post", 10000)
    data_charset = kwargs.get("data_charset", "".join(chr(x) for x in range(256)))
    joiner = kwargs.get("joiner", random.choice(default_delim))

    return joiner.join(
        [
            "".join(random.choice(data_charset) for _ in range(length_pre))
            + random.choice(delim_pre)
            + item
            + random.choice(delim_post)
            + "".join(random.choice(data_charset) for _ in range(length_post))
            for item in patterns
        ]
    )


def save_to_archives(data_, dir_path, name):
    with gzip.open(os.path.join(dir_path, name + ".gz"), "wb") as g:
        g.write(data_)

    with zipfile.ZipFile(os.path.join(dir_path, name + ".zip"), "w") as g:
        g.writestr("data", data_)

    with open(os.path.join(dir_path, name + ".br"), "wb") as g:
        g.write(brotli.compress(data_))

    with open(os.path.join(dir_path, name + ".bz2"), "wb") as g:
        g.write(bz2.compress(data_))

    with tarfile.open(os.path.join(dir_path, name + ".tar"), "w") as g:
        tarinfo = tarfile.TarInfo("data")
        tarinfo.size = len(data_)
        g.addfile(tarinfo=tarinfo, fileobj=BytesIO(data_))

    with tarfile.open(os.path.join(dir_path, name + ".tar.gz"), "w|gz") as g:
        tarinfo = tarfile.TarInfo("data")
        tarinfo.size = len(data_)
        g.addfile(tarinfo=tarinfo, fileobj=BytesIO(data_))

    with tarfile.open(os.path.join(dir_path, name + ".tar.bz2"), "w|bz2") as g:
        tarinfo = tarfile.TarInfo("data")
        tarinfo.size = len(data_)
        g.addfile(tarinfo=tarinfo, fileobj=BytesIO(data_))

    with tarfile.open(os.path.join(dir_path, name + ".tar.xz"), "w|xz") as g:
        tarinfo = tarfile.TarInfo("data")
        tarinfo.size = len(data_)
        g.addfile(tarinfo=tarinfo, fileobj=BytesIO(data_))


def save_to_files(out_data, dir_path, name):
    out_data_encoded = out_data.encode()
    with open(os.path.join(dir_path, name + ".dat"), "wb") as f:
        f.write(out_data_encoded)
    save_to_archives(out_data_encoded, dir_path, name + ".dat")

    base16_data = binascii.hexlify(out_data_encoded)
    with open(os.path.join(dir_path, name + ".base16"), "wb") as g:
        g.write(base16_data)
    # save_to_archives(base32_data, dir_path, name + ".base32")

    base32_data = base64.b32encode(out_data_encoded)
    with open(os.path.join(dir_path, name + ".base32"), "wb") as g:
        g.write(base32_data)
    # save_to_archives(base32_data, dir_path, name + ".base32")

    # base58_data = base58.b58encode(out_data_encoded)
    # with open(os.path.join(dir_path, name + ".base58"), "wb") as g:
    #     g.write(base58_data)
    # save_to_archives(base58_data, dir_path, name + ".base58")

    base64_data = base64.b64encode(out_data_encoded)
    with open(os.path.join(dir_path, name + ".base64"), "wb") as g:
        g.write(base64_data)
    # save_to_archives(base64_data, dir_path, name + ".base64")

    base85_data = base64.b85encode(out_data_encoded)
    with open(os.path.join(dir_path, name + ".base85"), "wb") as g:
        g.write(base85_data)
    # save_to_archives(base85_data, dir_path, name + ".base85")

    ascii85_data = base64.a85encode(out_data_encoded)
    with open(os.path.join(dir_path, name + ".ascii85"), "wb") as g:
        g.write(ascii85_data)
    # save_to_archives(ascii85_data, dir_path, name + ".ascii85")

    res = out_data_encoded + b"=" * ((4 - len(out_data_encoded) & 3) & 3)
    z85_data = z85.encode(res)
    with open(os.path.join(dir_path, name + ".z85"), "wb") as g:
        g.write(z85_data)
    # save_to_archives(z85_data, dir_path, name + ".z85")

    base91_data = base91.encode(out_data_encoded).encode()
    with open(os.path.join(dir_path, name + ".base91"), "wb") as g:
        g.write(base91_data)
    # save_to_archives(base91_data, dir_path, name + ".base91")

    uu_data = codecs.encode(out_data_encoded, encoding="uu")
    with open(os.path.join(dir_path, name + ".uu"), "wb") as g:
        g.write(uu_data)
    # save_to_archives(uu_data, dir_path, name + ".uu")

    quopri_data = quopri.encodestring(out_data_encoded)
    with open(os.path.join(dir_path, name + ".quopri"), "wb") as g:
        g.write(quopri_data)
    # save_to_archives(quopri_data, dir_path, name + ".quopri")

    binhex.binhex(
        os.path.join(dir_path, name + ".dat"), os.path.join(dir_path, name + ".binhex")
    )
    # with open(os.path.join(dir_path, name + ".binhex"), "rb") as g:
    #     binhex_data = g.read()
    # save_to_archives(binhex_data, dir_path, name + ".binhex")


if __name__ == "__main__":
    input_data = {
        "btc_adress": get_btc_addresses(),
        "btc_xkeys": get_btc_xkeys(),
        "btc_wif": get_btc_wif(),
        "bch_addresses": get_bitcoincash_addresses(),
        "ripple": get_ripple_addresses(),
        "litecoin": get_litecoin_addresses(),
        "ethereum": get_ethereum_addresses(),
        "cardano": get_cardano_addresses(),
        "polkadot": get_polkadot_addresses(),
        "ipv4": get_ipv4_addresses(),
        "ipv6": get_ipv6_addresses(),
        "emails": get_email_addresses(),
        "md5s": get_md5_digests(),
        "urls": get_urls(),
        "data_uris": get_data_uris(),
        "base_64": get_base64(),
        "base_32": get_base32(),
        "sha_1": get_sha1_digests(),
        "sha_224": get_sha224_digests(),
        "sha_256": get_sha256_digests(),
        "sha_384": get_sha384_digests(),
        "sha_512": get_sha512_digests(),
        "mac": get_mac_addresses(),
        "isbn10": get_isbn10(),
        "isbn13": get_isbn13(),
        "issn": get_issn(),
        "dois": get_dois(),
        "magnets": get_magnet_links(),
        "tether": get_tether_addresses(),
        "guids": get_guids(),
        "urns": get_urns(),
        "email_multipart": get_email_msgs(),
        "chainlink": get_chainlink_addresses(),
        "pems": get_pems(),
        "stellar": get_stellar_addresses(),
    }
    input_data["ips"] = input_data["ipv4"] + input_data["ipv6"]
    input_data["isbn"] = input_data["isbn10"] + input_data["isbn13"]

    generated_data = {
        k: create_random_data_with_patterns(v) for k, v in input_data.items()
    }
    delim = string.punctuation + string.digits + string.ascii_letters
    generated_data_ambiguous = {
        k: create_random_data_with_patterns(v, delim_pre=delim, delim_post=delim)
        for k, v in input_data.items()
    }

    path_input_simple = os.path.join("test_data", "input", "simple")
    path_individual_simple = os.path.join(path_input_simple, "individual")
    path_all_simple = os.path.join(path_input_simple, "all")

    path_input_ambiguous = os.path.join("test_data", "input", "ambiguous")
    path_individual_ambiguous = os.path.join(path_input_ambiguous, "individual")
    path_all_ambiguous = os.path.join(path_input_ambiguous, "all")

    os.makedirs(path_individual_simple, exist_ok=True)
    os.makedirs(path_all_simple, exist_ok=True)
    os.makedirs(path_individual_ambiguous, exist_ok=True)
    os.makedirs(path_all_ambiguous, exist_ok=True)

    for _type, _data in generated_data.items():
        save_to_files(_data, path_individual_simple, _type)

    save_to_files("".join(d for d in generated_data.values()), path_all_simple, "data")

    for _type, _data in generated_data_ambiguous.items():
        save_to_files(_data, path_individual_ambiguous, _type)

    save_to_files(
        "".join(d for d in generated_data_ambiguous.values()),
        path_all_ambiguous,
        "data",
    )

# to create yEnc demo encoded output, use https://www.webutils.pl/yEnc
