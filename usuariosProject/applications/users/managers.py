# DJango imports
from django.db import models

#DJango managers imports
from django.contrib.auth.models import BaseUserManager


# Managers

class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):

        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )

        # Encrypt the password
        user.set_password(password)

        # Save user in database
        user.save(using=self.db)

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):

        staff, superuser = True, True
        return self._create_user(username, email, password, staff, superuser, **extra_fields)
        



    