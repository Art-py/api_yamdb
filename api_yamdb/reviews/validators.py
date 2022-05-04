from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class UsernameValidator(RegexValidator):
    regex = r'^[\w.@+-]{1,150}$'
    message=(
        'Не более 150 символов, '
        'допустимы только буквы, цифры и @/./+/-/_'
    )
    exception = None

    def __call__(self, value):
        try:
            super().__call__(value)
            if value == 'me':
                raise ValidationError('Имя пользователя me не может быть использовано', code='invalid')
        except ValidationError as e:
            if self.exception:
                raise self.exception(e.message, code=e.code)
            raise
