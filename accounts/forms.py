from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

class CustomUserCreationForm(UserCreationForm):
    
    # email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'type', 'password1', 'password2']

        labels = {
            'email':'آدرس ایمیل',
            'username':'نام کاربری',
            'type':'نوع کاربر',
        }

           

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'type',)


class CustomAuthenticationForm(AuthenticationForm):
    
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        self.fields['username'].label = 'نام کاربری'
        self.fields['password'].label = 'رمز عبور'