import random


def generate_verification_code():
    """Generate a unique random number of specified length."""
    length = 6
    range_start = 10 ** (length - 1)
    range_end = (10**length) - 1
    return str(random.randint(range_start, range_end))
