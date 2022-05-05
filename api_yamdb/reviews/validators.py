import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

USERNAME_REGEX = re.compile(r'^[\w.@+-]+$')


def validate_username(value):
    if not USERNAME_REGEX.match(value):
        raise ValidationError(
            message='допустимы только буквы, цифры и @/./+/-/_',
            code='invalid'
        )
    if value == 'me':
        raise ValidationError(
            'Имя пользователя me не может быть использовано',
            code='invalid'
        )
