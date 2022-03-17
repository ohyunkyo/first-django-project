import re

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_alpha_num(value):
    matches = re.match('[a-zA-Z0-9]*$', value)
    if matches is None:
        raise ValidationError(
            '영문과 숫자만 사용 가능합니다',
            params={'value': value},
        )


def validate_phone_number(value):
    matches = re.match('010[2-9][0-9]{7}$', value)
    if matches is None:
        raise ValidationError(
            '잘못된 전화번호입니다',
            params={'value': value},
        )