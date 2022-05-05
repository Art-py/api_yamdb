from rest_framework import serializers

import reviews.validators


class UsernameValidator(reviews.validators.UsernameValidator):
    exception = serializers.ValidationError
