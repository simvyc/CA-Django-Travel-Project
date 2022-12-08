from django import forms
from .models import Account
from . import views

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'example@email.com',
        'class': 'form-control',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }))
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password', 'phone_number']
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = '+37061101010'
        self.fields['email'].widget.attrs['placeholder'] = 'example@email.com'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
                
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords does not match :)")