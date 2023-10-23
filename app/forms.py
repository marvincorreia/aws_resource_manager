from .models import AWSAccount, Notification
from django import forms


class AWSAccountForm(forms.ModelForm):
    class Meta:
        model = AWSAccount
        fields = '__all__'
        widgets = {
            'aws_secret_access_key': forms.PasswordInput(),
        }

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'
        widgets = {
            'auth_password': forms.PasswordInput(),
        }

