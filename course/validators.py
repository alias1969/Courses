from rest_framework.validators import ValidationError


def url_validator(value):
    if not value:
        return None
    elif "youtube.com" not in value:
        raise ValidationError("Разрешены ссылки только с youtube.com")
