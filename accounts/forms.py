from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-input', 'placeholder': 'you@college.edu'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'First name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'student_id',
            'department', 'year', 'phone', 'password1', 'password2',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Choose a username'}),
            'student_id': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 2024CSE045'}),
            'department': forms.Select(attrs={'class': 'form-input'}),
            'year': forms.Select(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '10-digit phone number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Create a password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirm password'})


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Username', 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Password'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'department', 'year', 'phone', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'department': forms.Select(attrs={'class': 'form-input'}),
            'year': forms.Select(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-input-file'}),
        }
