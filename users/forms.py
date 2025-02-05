from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'w-full bg-gray-50 rounded-lg py-3 px-12 outline-none focus:ring-2 focus:ring-purple-500 transition-all',
                'placeholder': 'Ваш логин или почта',
                'id': 'username'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'w-full bg-gray-50 rounded-lg py-3 px-12 outline-none focus:ring-2 focus:ring-purple-500 transition-all',
                'placeholder': 'Пароль',
                'id': 'password'
            }
        )
    )
    error_messages = {
        'invalid_login': 'Пожалуйста, введите правильные имя пользователя или пароль.',
        'inactive': 'Этот аккаунт не активен.',
    }

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'w-full bg-gray-50 rounded-lg py-3 px-12 outline-none focus:ring-2 focus:ring-purple-500 transition-all',
                'placeholder': 'Ваш логин',
                'id': 'username'
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'w-full bg-gray-50 rounded-lg py-3 px-12 outline-none focus:ring-2 focus:ring-purple-500 transition-all',
                'placeholder': 'Пароль',
                'id': 'password1'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'w-full bg-gray-50 rounded-lg py-3 px-12 outline-none focus:ring-2 focus:ring-purple-500 transition-all',
                'placeholder': 'Повторите пароль',
                'id': 'password2'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'w-full bg-gray-50 rounded-lg py-3 px-12 outline-none focus:ring-2 focus:ring-purple-500 transition-all',
                'placeholder': 'Ваша электронная почта',
                'id': 'email'
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким Email уже существует')
        return email


class VerifForm(forms.Form):
    number = forms.CharField(
        min_length=6,
        max_length=6,
        widget=forms.TextInput(
            attrs={
                'name': 'code',
                'class': 'w-72 h-12 rounded-lg border-2 border-neutral-200 text-center text-xl font-semibold focus:border-primary-500 focus:outline-none transition-colors',
                'oninput': 'moveFocus(this)',
                'autofocus': 'autofocus'
            }
        )
    )
