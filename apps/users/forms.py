from allauth.account.forms import SignupForm
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Profile


# https://docs.allauth.org/en/latest/account/forms.html
class MyCustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')

        try:
            user.save()
        except Exception as e:
            # Handle the exception, e.g., log it or notify the user
            raise forms.ValidationError(_("An error occurred while saving the user details."))

        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'preferred_language',
            'preferred_communication_method',
            'additional_phone_number', 
            'emergency_contact_name', 
            'emergency_contact_phone', 
        ]