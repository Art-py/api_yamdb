import re
import datetime as dt

from django.core.exceptions import ValidationError

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

    def __call__(self, value):
        try:
            super().__call__(value)
            if value == 'me':
                raise ValidationError(
                    'Имя пользователя me не может быть использовано',
                    code='invalid'
                )
        except ValidationError as e:
            if self.exception:
                raise self.exception(e.message, code=e.code)
            raise


def no_future_year(value):
    if value > dt.date.today().year:
        raise ValidationError(
            f'Год выхода произведения: {value}, не может быть больше текущего!'
        )
