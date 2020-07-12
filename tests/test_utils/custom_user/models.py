from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    @property
    def email(self):
        return "some@example.com"
