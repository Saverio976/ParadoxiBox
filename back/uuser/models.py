from typing import Any, Optional
from django.db import models
import secrets

import hashlib

# Create your models here.

LENGTH_BEARER = 32

class UUser(models.Model):
    bearer = models.CharField(max_length=LENGTH_BEARER, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=512)

    __original_pasword = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__original_pasword = self.password

    def save(self, *args, **kwargs):
        if self.password != self.__original_pasword or not self.pk:
            self.password = UUser.crypt(self.password)
        super().save(*args, **kwargs)

    @staticmethod
    def crypt(data: str) -> str:
        return hashlib.blake2s(data.encode()).hexdigest()

    @staticmethod
    def is_connected(bearer: str) -> bool:
        try:
            UUser.objects.get(bearer=bearer)
        except:
            return False
        return True

    @staticmethod
    def disconnect(bearer: str):
        user = UUser.objects.get(bearer=bearer)
        user.bearer = None
        user.save()

    @staticmethod
    def connect(email: str, password: str) -> Optional['UUser']:
        password = UUser.crypt(password)
        try:
            user = UUser.objects.get(email=email, password=password)
        except Exception:
            return None
        user.bearer = secrets.token_urlsafe(LENGTH_BEARER)
        try:
            user.save()
        except:
            user.bearer = secrets.token_urlsafe(LENGTH_BEARER)
            try:
                user.save()
            except Exception:
                return None
        return user

    @staticmethod
    def create(email: str, username: str, password: str) -> Optional['UUser']:
        try:
            user = UUser.objects.get(email=email)
            return None
        except:
            pass
        user = UUser(email=email, username=username, password=password)
        user.save()
        return user

    @staticmethod
    def delete_with_bearer(bearer: str) -> bool:
        try:
            user = UUser.objects.get(bearer=bearer)
            user.delete()
        except:
            return False
        return True
