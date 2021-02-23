from django import forms
from django.contrib.auth import get_user_model
from apps.main.users.models import CustomUser

ROLE_CHOICES =( 
    ("1", "Superuser"), 
    ("2", "Admin"), 
    ("3", "Analist"), 
    ("4", "Editor"), 
) 


class CustomUserForm(forms.ModelForm):
    role = forms.ChoiceField(choices = ROLE_CHOICES, required=True) 
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
        ]
