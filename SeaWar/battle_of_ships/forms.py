from django import forms
from battle_of_ships.models import *


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {
            "name",
        }

        widgets = {
            "name": forms.TextInput()
        }

        lables = {
            "name": "Enter You name my capitan"
        }