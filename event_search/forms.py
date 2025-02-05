from django import forms
from django.core.exceptions import ValidationError


class AddPostForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        min_length=3,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-neutral-300 rounded-md p-3 text-sm text-neutral-950 outline-none focus:ring-2 focus:ring-primary-500',
            'placeholder': 'Введите название мероприятия'})
    )
    place = forms.CharField(
        max_length=50,
        min_length=3,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-neutral-300 rounded-md p-3 text-sm text-neutral-950 outline-none focus:ring-2 focus:ring-primary-500',
            'placeholder': 'Введите место проведение, например название вашего города'})
    )
    wish = forms.CharField(
        max_length=255,
        min_length=5,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-neutral-300 rounded-md p-3 text-sm text-neutral-950 outline-none focus:ring-2 focus:ring-primary-500',
            'placeholder': 'Опишите ваши пожелания по организации мероприятия'}), required=False
    )
    agree = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'border border-neutral-300 rounded-md p-3 text-sm text-neutral-950 outline-none focus:ring-2 focus:ring-primary-500'},
        ),
        initial=True
    )


class SupportForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        min_length=3,
        widget=forms.TextInput(attrs={
            'placeholder': "Ваше имя",
            'class': "w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-violet-300 focus:ring-2 focus:ring-violet-100 outline-none transition-all duration-200"})
    )
    mail = forms.EmailField(
        max_length=50,
        min_length=3,
        widget=forms.TextInput(attrs={
            'placeholder': "Ваша почта",
            'class': "w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-violet-300 focus:ring-2 focus:ring-violet-100 outline-none transition-all duration-200"})
    )
    text = forms.CharField(
        min_length=3,
        widget=forms.Textarea(attrs={
            'placeholder': "Опишите ваш вопрос",
            'rows': "4",
            'class': "w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-violet-300 focus:ring-2 focus:ring-violet-100 outline-none transition-all duration-200 resize-none"})
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'hidden'
        })
    )
