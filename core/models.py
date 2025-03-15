import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseManager(UserManager):
    use_in_migrations = True

    def _create_user(self, public_key, **extra_fields):
        """
        Create and save a user with the given public key.
        """

        user = self.model(public_key=public_key, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, public_key, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(public_key, **extra_fields)

    def create_superuser(self, public_key, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(public_key, **extra_fields)


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("created_at",)

    @property
    def id_as_str(self) -> str:
        return str(self.id)


class User(AbstractUser, BaseModel):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(
        _("Email"),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    public_key = models.CharField(
        _("Public Key"),
        max_length=70,
        unique=True,
    )
    objects = BaseManager()

    USERNAME_FIELD = "public_key"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.public_key
