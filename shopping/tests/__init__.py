from django.test.utils import ignore_warnings

ignore_warnings(message="No directory at", module="whitenoise.base").enable()
