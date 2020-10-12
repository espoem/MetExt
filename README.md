# Extrakce Bitcoinových adres z base64 kódovaného vstupu

Kód pro detekci a extrakci validních Bitcoinových adres. Podporované adresy z mainnetu jsou:

- P2PKH začínající číslem 1, např. 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2
- P2SH začínající číslem 3, např. 3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy
- Bech32 začínající na bc1, např. bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq

Formátování kódu pomocí nástrojů `isort` a `black`.

## Použití

Zkoušeno s Python ve verzi 3.5.5.

```
python main.py <base64_file> [...base64_file]
```

Lze také přes rouru zpracovat standardní vstup.

### Příklad použití

```
python main.py examples\ex1_base64 examples\ex2_base64
```

Výstup

```
BTC addresses:
1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW62i
BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4
bc1zw508d6qejxtdg4y5r3zarvaryvg6kdaj
3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy
```

## Testy

Testy jsou psány pomocí `pytest`.

```
python -m pip install pytest
pytest Detector
```

## Neúplný seznam použitých informačních zdrojů

- http://rosettacode.org/wiki/Bitcoin/address_validation#Python
- https://github.com/niksmac/btc-validate/tree/master/src
- https://github.com/keis/base58
- https://en.bitcoin.it/wiki/Address
- https://en.bitcoin.it/wiki/Bech32
- https://en.bitcoin.it/wiki/BIP_0173
