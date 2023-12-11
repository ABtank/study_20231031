from django import forms
from .validators import russian_email
from django.core.validators import MinLengthValidator

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, FileInput, Select, CheckboxInput

from .models import Account


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {'username': TextInput({'class': 'textinput form-control',
                                          'placeholder': 'username'}),
                   'email': EmailInput({'class': 'textinput form-control',
                                        'placeholder': 'email'}),
                   'first_name': TextInput({'class': 'textinput form-control',
                                            'placeholder': 'First name'}),
                   'last_name': TextInput({'class': 'textinput form-control',
                                           'placeholder': 'Last name'}),
                   }


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['phone', 'address', 'vk', 'instagram', 'telegram', 'account_image',
                  'first_name',
                  'last_name',
                  'is_all_agree',
                  'is_all_inform',
                  ]
        widgets = {'phone': TextInput({'class': 'textinput form-control',
                                       'placeholder': 'phone number', 'required': False}),
                   'address': TextInput({'class': 'textinput form-control',
                                         'placeholder': 'address'}),
                   'vk': TextInput({'class': 'textinput form-control',
                                    'placeholder': 'vk'}),
                   'instagram': TextInput({'class': 'textinput form-control',
                                           'placeholder': 'instagram'}),
                   'telegram': TextInput({'class': 'textinput form-control',
                                          'placeholder': 'telegram'}),
                   'account_image': FileInput({'class': 'form-control',
                                               'placeholder': 'image'}),
                   'first_name': TextInput({'class': 'form-control',
                                               'placeholder': 'Имя'}),
                   'last_name': TextInput({'class': 'form-control',
                                               'placeholder': 'Фамилия'}),
                   'is_all_agree': CheckboxInput({'class': 'form-check-input'}),
                   'is_all_inform': CheckboxInput({'class': 'form-check-input'}),
                   }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100,
                           validators=[MinLengthValidator(2)],
                           initial='')
    email = forms.EmailField(
        validators=[russian_email]
    )
    message = forms.CharField(widget=forms.Textarea, disabled=False)
    demo = forms.BooleanField(required=False, help_text='Текст-подсказка',
                              label='Вам нравится?',
                              initial=True)
