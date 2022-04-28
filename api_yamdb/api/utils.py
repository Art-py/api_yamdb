import random
import string


def generate_confirmation_code(length=6):
    code = ''.join(random.choice(string.digits) for i in range(length))
    return code
