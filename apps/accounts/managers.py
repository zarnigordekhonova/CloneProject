from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, full_name, phone_number, password =None, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone number must be set")

        user = self.model(
            full_name=full_name,
            phone_number=phone_number,
            **extra_fields,
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user
    
    def create_user(self, full_name, phone_number, password=None, **extra_fields):
        """For creating a regular user"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if "country" not in extra_fields or extra_fields["country"] in [None, ""]:
            raise ValueError("User must choose a country.")

        return self._create_user(phone_number, full_name, password, **extra_fields)

    def create_superuser(self, full_name, phone_number, password, country=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_confirmed", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("country", None)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_confirmed") is not True:
            raise ValueError("Superuser must have is_confirmed=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if not password:
            raise ValueError("Superuser must have a password.")

        return self._create_user(full_name, phone_number, password, **extra_fields)