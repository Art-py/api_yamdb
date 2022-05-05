import random
import string

CONFIRMATION_CODE_CHARACTERS = string.digits + string.ascii_letters


def generate_confirmation_code(length):
    return ''.join(
        random.choice(CONFIRMATION_CODE_CHARACTERS) for _ in range(length)
    )
