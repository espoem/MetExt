import textwrap
from datetime import datetime
from typing import Optional

from Crypto.Util.asn1 import DerObject, DerSequence
from OpenSSL.crypto import (
    FILETYPE_ASN1,
    FILETYPE_PEM,
    TYPE_DSA,
    TYPE_RSA,
    dump_certificate,
    dump_privatekey,
    load_certificate,
)

from metext.plugin_base import BaseDecoder, Decodable


class PemDecoder(BaseDecoder):
    PLUGIN_NAME = "pem"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes PEM certificate as bytes containing
         certificate info.

        :param _input: String or bytes
        :param kwargs:
        :return: Bytes string if decoded successfully, else None
        """
        try:
            return parse_cert(
                bytes(_input, "utf8") if isinstance(_input, str) else _input
            )
        except:
            return None


# credit: http://www.zedwood.com/article/python-openssl-x509-parse-certificate
def format_subject_issuer(x509name):
    return ", ".join(
        "{}={}".format(item[0], item[1]) for item in x509name.get_components()
    )


def format_split_bytes(aa):
    bb = (
        aa[1:] if len(aa) % 2 == 1 else aa
    )  # force even num bytes, remove leading 0 if necessary
    return format(":".join("{:02x}".format(s) for s in (bytes.fromhex(bb))))


def format_split_int(serial_number):
    aa = "0{:x}".format(serial_number)  # add leading 0
    return format_split_bytes(aa)


def format_asn1_date(d):
    return datetime.strptime(d.decode("ascii"), "%Y%m%d%H%M%SZ").strftime(
        "%Y-%m-%d %H:%M:%S GMT"
    )


def get_signature_bytes(x509):
    der = DerSequence()
    der.decode(dump_certificate(FILETYPE_ASN1, x509))
    der_tbs = der[0]
    der_algo = der[1]
    der_sig = der[2]
    der_sig_in = DerObject()
    der_sig_in.decode(der_sig)
    sig = der_sig_in.payload[1:]  # skip leading zeros
    return sig.hex()


def get_modulus_and_exponent(x509):
    if x509.get_pubkey().type() == TYPE_RSA:
        pub_der = DerSequence()
        privatekey = dump_privatekey(FILETYPE_ASN1, x509.get_pubkey())
        pub_der.decode(privatekey)
        modulus = "{}:{}".format(
            format_split_int(pub_der._seq[0]), format_split_int(pub_der._seq[1])
        )
        exponent = pub_der._seq[2]
        return [modulus, exponent]
    return ""


def parse_cert(cert_pem):
    x509 = load_certificate(FILETYPE_PEM, cert_pem)

    keytype = x509.get_pubkey().type()
    keytype_list = {
        TYPE_RSA: "rsaEncryption",
        TYPE_DSA: "dsaEncryption",
        408: "id-ecPublicKey",
    }
    key_type_str = keytype_list[keytype] if keytype in keytype_list else "other"

    pkey_lines = [
        "        Public Key Algorithm: {}".format(key_type_str),
        "            Public-Key: ({} bit)".format(x509.get_pubkey().bits()),
    ]

    if x509.get_pubkey().type() == TYPE_RSA:
        modulus, exponent = get_modulus_and_exponent(x509)
        formatted_modulus = "\n                ".join(textwrap.wrap(modulus, 45))
        pkey_lines.append("            Modulus:")
        pkey_lines.append("                {}".format(formatted_modulus))
        pkey_lines.append(
            "            Exponent {:d} (0x{:x})".format(exponent, exponent)
        )
    sig_formatted = "\n         ".join(
        textwrap.wrap(format_split_bytes(get_signature_bytes(x509)), 54)
    )

    res = [
        "Certificate:",
        "    Data:",
        "        Version: {} (0x{:x})".format(
            int(x509.get_version() + 1), x509.get_version()
        ),
        "        Serial Number:",
        "            {}".format(format_split_int(x509.get_serial_number())),
        "    Signature Algorithm: {}".format(x509.get_signature_algorithm()),
        "    Issuer: {}".format(format_subject_issuer(x509.get_issuer())),
        "    Validity",
        "        Not Before: {}".format(format_asn1_date(x509.get_notBefore())),
        "        Not After : {}".format(format_asn1_date(x509.get_notAfter())),
        "    Subject: {}".format(format_subject_issuer(x509.get_subject())),
        "    Subject Public Key Info:",
        "\n".join(pkey_lines),
        "        X509v3 extensions:",
    ]

    for i in range(x509.get_extension_count()):
        critical = "critical" if x509.get_extension(i).get_critical() else ""
        res.append(
            "             x509v3 {}: {}".format(
                x509.get_extension(i).get_short_name(), critical
            )
        )
        for ex in x509.get_extension(i).__str__().split(sep="\n"):
            res.append("                 {}".format(ex))
    res.append("    Signature Algorithm: {}".format(x509.get_signature_algorithm()))
    res.append("         {}".format(sig_formatted))
    res.append("    Thumbprint MD5:    {}".format(x509.digest("md5")))
    res.append("    Thumbprint SHA1:   {}".format(x509.digest("sha1")))
    res.append("    Thumbprint SHA256: {}".format(x509.digest("sha256")))
    return bytes("\n".join(res), "utf8")
