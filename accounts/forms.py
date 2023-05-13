from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,UserStandard
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )






class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    local= forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    ntelefono = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name' ,'is_client', 'is_admin',)





class editUserForm(forms.Form):

    username = forms.CharField( max_length=255, min_length=2, 
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    firstname = forms.CharField( max_length= 100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )


    def clean_username(self):
        username = self.cleaned_data['username']
        if username == "nombre":
            print("igual")
            ValidationError('""')
        else:
            print("no igual")
            return username

