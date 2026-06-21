BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62_ALPHABET[0]
    digits = []
    while num:
        num, rem = divmod(num, 62)
        digits.append(BASE62_ALPHABET[rem])
    return "".join(reversed(digits))