from django import forms
from .models import UserProfile

from .encrypt_helper import encrypt_password


class UserProfileForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False,
                                   label="Новый пароль")

    class Meta:
        model = UserProfile
        fields = ['photo', 'etu_email']

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user_profile.etu_password_encrypted = encrypt_password(new_password)
        if commit:
            user_profile.save()
        return user_profile

    def clean_etu_password_encrypted(self):
        """Encrypt the password before it's saved to the database."""
        password = self.cleaned_data.get('etu_password_encrypted')
        if password:
            return encrypt_password(password)
        return password

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user_profile.etu_password_encrypted = self.cleaned_data['etu_password_encrypted']
        if commit:
            user_profile.save()
        return user_profile
