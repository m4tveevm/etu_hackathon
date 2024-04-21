from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    etu_session_data = models.TextField()
    etu_email = models.EmailField(default='')
    etu_password_encrypted = models.CharField(max_length=255, blank=True, null=True, default='')

    def __str__(self):
        return self.user.username

    def set_password(self, raw_password):
        """Зашифровать и сохранить пароль"""
        self.etu_password_encrypted = cipher.encrypt(raw_password.encode()).decode()
        self.save()

    def get_password(self):
        """Расшифровать и вернуть пароль"""
        if self.etu_password_encrypted:
            return cipher.decrypt(self.etu_password_encrypted.encode()).decode()
        return None

    @staticmethod
    def ready():
        # Импорт сигналов
        from . import signals


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
