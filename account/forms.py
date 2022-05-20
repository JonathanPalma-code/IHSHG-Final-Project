from django import forms
from django.contrib.auth.models import User
from account.models import Profile
from django.contrib.auth.forms import PasswordResetForm


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
    }))

class LoginForm(forms.Form):
    username = forms.CharField(label='',
                                widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class UserRegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    # Loop to display all fields 
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
            self.fields[field_name].label = ''

    # Label needs to be defined because of the loop
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    password2 = forms.CharField(label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    # Clean both fields if it is not a match
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    
    # Disabled email field
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].widget.attrs['disabled'] = True

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
