from django.forms import ModelForm
from .models import UserProfile
from .encrypt_helper import encrypt_password


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo', 'etu_email',
                  'etu_password_encrypted']

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
