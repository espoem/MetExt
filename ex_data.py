import base64
import random
from string import printable

if __name__ == "__main__":
    btc_addresses = [
        "1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW62i",
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
        "BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4",
        "bc1q5s8fz9p8x0a59774jlr9cmuwf6kjdv3j5tqvxm",
        "3Fxq8ctmbr5CQEdoow189rAi64LePvxgfb",
    ]
    result = []
    for address in btc_addresses:
        result += ["".join(random.choice(printable) for i in range(1000000)), address]

    with open("examples/ex_input.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(result))

    with open("examples/ex_base64", "wb") as g:
        g.write(base64.b64encode("\n".join(result).encode("utf-8")))
