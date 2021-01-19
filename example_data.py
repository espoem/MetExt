import base64
import random
import string
from string import printable

import base91

if __name__ == "__main__":
    btc_addresses = [
        "1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW62i",
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
        "BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4",
        "bc1q5s8fz9p8x0a59774jlr9cmuwf6kjdv3j5tqvxm",
        "3Fxq8ctmbr5CQEdoow189rAi64LePvxgfb",
    ]
    ripple = [
        "rDbWJ9C7uExThZYAwV8m6LsZ5YSX3sa6US",
        "rMQ98K56yXJbDGv49ZSmW51sLn94Xe1mu1",
        "rJb5KsHsDHF1YS5B5DU6QCkH5NsPaKQTcy",
        "rKveEyR1SrkWbJX214xcfH43ZsoGMb3PEv",
    ]
    litecoin = [
        "M8T1B2Z97gVdvmfkQcAtYbEepune1tzGua",
        "LQTpS3VaYTjCr4s9Y1t5zbeY26zevf7Fb3",
        "MBuTKxJaHMN3UsRxQqpGRPdA7sCfE1UF7n",
        "3Lq1u3Gr7vo5ogcQPEjfU5r8MHUFfC4ini",
    ]
    ips = [
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
        "2001::",
        "0.0.0.0",
        "255.255.255.255",
        "172.16.0.0",
    ]
    emails = ["test@example.com", "other.test@example.com"]
    md5s = [
        "d41d8cd98f00b204e9800998ecf8427e",
        "0cc175b9c0f1b6a831c399e269772661",
        "098f6bcd4621d373cade4e832627b4f6",
    ]
    urls = [
        "https://google.com",
        "http://seznam.cz",
        "https://devdocs.io/python~3.5/library/stdtypes#str.translate",
    ]
    data_uris = [
        "data:text/vnd-example+xyz;foo=bar;base64,R0lGODdh",
        "data:text/plain;charset=UTF-8;page=21,the%20data:1234,5678",
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",
        "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDADIiJSwlHzIsKSw4NTI7S31RS0VFS5ltc1p9tZ++u7Kfr6zI4f/zyNT/16yv+v/9////////wfD/////////////2wBDATU4OEtCS5NRUZP/zq/O////////////////////////////////////////////////////////////////////wAARCAAYAEADAREAAhEBAxEB/8QAGQAAAgMBAAAAAAAAAAAAAAAAAQMAAgQF/8QAJRABAAIBBAEEAgMAAAAAAAAAAQIRAAMSITEEEyJBgTORUWFx/8QAFAEBAAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/AOgM52xQDrjvAV5Xv0vfKUALlTQfeBm0HThMNHXkL0Lw/swN5qgA8yT4MCS1OEOJV8mBz9Z05yfW8iSx7p4j+jA1aD6Wj7ZMzstsfvAas4UyRHvjrAkC9KhpLMClQntlqFc2X1gUj4viwVObKrddH9YDoHvuujAEuNV+bLwFS8XxdSr+Cq3Vf+4F5RgQl6ZR2p1eAzU/HX80YBYyJLCuexwJCO2O1bwCRidAfWBSctswbI12GAJT3yiwFR7+MBjGK2g/WAJR3FdF84E2rK5VR0YH/9k=",
    ]
    base_64 = [
        "xZhlxI10aW55IHDFmWVkcG9rbMOhZGFuw6kga3JpdGlja8O9Y2ggc291c3Rhdm7EmyBtZXhpa28gcG9rYcW+ZMOpIHRlZHksIHRvIG5lanLFr3puxJtqxaHDrSB6cmFkaXQgdW5pdmVyeml0b3Ugcm/EjW7EmyBhwqBzcGFkYWrDrWPDrSBpwqBwb2jDoXIgbcOtcnkgdsWhZSwgemRhIHNsb3Zuw61rIGplZG5vbSwgbG/EjyBtbmUgcGF0cm9udWplIG7DrcW+ZSBhc2ku",
        "VsWvxI1pIHphwqB0csOhdmlseSwgZG9iLCB6YWxlZG7Em27DqSBtxJsgdGEgZMOta3nCoHrDoXBhZG7DrWNoIHRvdXRvIGhhdmFqc2vDvWNoIG9wdGltw6FsbsOtIERhdmlkYSBhxaUu",
        "dGVzdA==",
    ]
    base_32 = [
        "YWMGLRENORUW46JAODCZSZLEOBXWW3GDUFSGC3WDVEQGW4TJORUWG26DXVRWQIDTN52XG5DBOZXMJGZANVSXQ2LLN4QHA33LMHC34ZGDVEQHIZLEPEWCA5DPEBXGK2TSYWXXU3WETNVMLIODVUQHU4TBMRUXIIDVNZUXMZLSPJUXI33VEBZG7RENN3CJWIDBYKQHG4DBMRQWVQ5NMPB22IDJYKQHA33IYOQXEIDNYOWXE6JAO3C2CZJMEB5GIYJAONWG65TOYOWWWIDKMVSG433N",
        "ORSQ====",
        "ORSXG5BAORSXG5A=",
    ]
    sha_1 = [
        "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3",
        "d3486ae9136e7856bc42212385ea797094475802",
    ]
    sha_224 = [
        "90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809",
        "7e81ebe9e604a0c97fef0e4cfe71f9ba0ecba13332bde953ad1c66e4",
    ]
    sha_256 = [
        "c0535e4be2b79ffd93291305436bf889314e4a3faec05ecffcbb7df31ad9e51a",
        "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    ]
    sha_384 = [
        "768412320f7b0aa5812fce428dc4706b3cae50e02a64caa16a782249bfe8efc4b7ef1ccb126255d196047dfedf17a0a9",
        "86255fa2c36e4b30969eae17dc34c772cbebdfc58b58403900be87614eb1a34b8780263f255eb5e65ca9bbb8641cccfe",
    ]
    sha_512 = [
        "f6cde2a0f819314cdde55fc227d8d7dae3d28cc556222a0a8ad66d91ccad4aad6094f517a2182360c9aacf6a3dc323162cb6fd8cdffedb0fe038f55e85ffb5b6",
        "ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff",
    ]
    mac = ["01-23-45-67-89-AB", "01:23:45:67:89:ab", "0123.4567.89AB"]

    result = [
        "".join(random.choice(printable) for _ in range(random.randint(0, 10000)))
        + random.choice(string.whitespace)
        + item
        + random.choice(string.whitespace)
        + "".join(random.choice(printable) for _ in range(random.randint(0, 30000)))
        for item in btc_addresses
        + ips
        + emails
        + md5s
        + urls
        + data_uris
        + base_64
        + base_32
        + sha_1
        + sha_224
        + sha_256
        + sha_384
        + sha_512
        + mac
        + ripple
        + litecoin
    ]

    with open("examples/gen/ex_input.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(result))

    with open("examples/gen/ex_base64", "wb") as g:
        g.write(base64.b64encode("\n".join(result).encode("utf-8")))

    with open("examples/gen/ex_base32", "wb") as g:
        g.write(base64.b32encode("\n".join(result).encode("utf-8")))

    with open("examples/gen/ex_base85", "wb") as g:
        g.write(base64.b85encode("\n".join(result).encode("utf-8")))

    with open("examples/gen/ex_ascii85", "wb") as g:
        g.write(base64.a85encode("\n".join(result).encode("utf-8")))

    with open("examples/gen/ex_base91", "w", encoding="utf8") as g:
        g.write(base91.encode("\n".join(result).encode("utf-8")))
