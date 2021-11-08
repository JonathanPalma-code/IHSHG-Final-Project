from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    birth_date = models.DateField()
    is_active = models.BooleanField(default=False)
    reports = models.IntegerField(default=0)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'birth date': self.dateFormat(),
            'is_active': self.is_active,
            'reports': self.reports,
        }

    def dateFormat(self):
        if self.birth_date:
            return self.birth_date.strftime('%b %#d %Y')

    def __str__(self):
        return f'{self.email}'
