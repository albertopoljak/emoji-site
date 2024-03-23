import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


WORD_REGEX_PATTERN = re.compile("^[a-z]+$")


def validate_word_name(value: str):
    if not re.match(WORD_REGEX_PATTERN, value):
        raise ValidationError(
            _("%(value) is not valid! Only lowercase a-z letters are allowed."),
            params={"value": value},
        )
