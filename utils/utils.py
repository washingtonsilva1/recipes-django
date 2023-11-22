from random import SystemRandom
import string


def generate_random_string(n=5) -> str:
    chars = string.ascii_letters + string.digits
    rand = SystemRandom().choices(population=chars, k=n)
    return ''.join(rand)
