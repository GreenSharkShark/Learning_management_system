from rest_framework.serializers import ValidationError


class URLValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = dict(value).get(self.field)
        if 'youtube.com' not in url:
            raise ValidationError('Ссылки на сторонние ресурсы кроме "youtube.com" запрещены.')
