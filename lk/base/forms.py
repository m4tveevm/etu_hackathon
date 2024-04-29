from django import forms
from .models import UserProfile
from .encrypt_helper import encrypt_password


class UserProfileForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(), required=False, label="Пароль от lk.etu.ru"
    )

    class Meta:
        model = UserProfile
        fields = ["photo", "etu_email"]

    def clean_password(self):
        """Encrypt the password before it's saved to the database."""
        password = self.cleaned_data.get("password")
        if password:
            return encrypt_password(password)
        return password

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        encrypted_password = self.cleaned_data.get("password")
        if encrypted_password:
            user_profile.etu_password_encrypted = encrypted_password

        if commit:
            user_profile.save()
        return user_profile
