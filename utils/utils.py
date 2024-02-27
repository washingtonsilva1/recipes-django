from random import SystemRandom
import string


def generate_random_string(n=5) -> str:
    chars = string.ascii_letters + string.digits
    rand = SystemRandom().choices(population=chars, k=n)
    return ''.join(rand)


def parse_str_to_list(string: str, sep=',') -> list:
    if not string or not isinstance(string, str):
        return []
    if not sep or not isinstance(sep, str):
        sep = ','
    return [s.strip() for s in string.split(sep) if s.strip()]


def parse_str_to_int(string: str) -> int:
    try:
        return int(string)
    except (ValueError, TypeError):
        return -1
