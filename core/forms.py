from django import forms

class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=True,
        label="User name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter username'})
    )

    password = forms.CharField(
        max_length=20,
        required=True,
        label="Password",
        widget=forms.PasswordInput()
    )
