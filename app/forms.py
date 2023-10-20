from .models import AWSAccount, CronJob
from django import forms


class AWSAccountForm(forms.ModelForm):
    class Meta:
        model = AWSAccount
        fields = '__all__'
        widgets = {
            'aws_secret_access_key': forms.PasswordInput(),
        }


# class CronField(forms.CharField):
#     widget = forms.TextInput(attrs={'placeholder': '0 6 * * 1-5'})


# class CronAdminForm(forms.ModelForm):
#     cron_schedule = CronField(required=False)  # Add the field name as per your model

#     class Meta:
#         model = CronJob  # Replace with your model name
#         fields = '__all__'
