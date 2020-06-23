from django import  forms
from app.models import *


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'minlength': 5, 'maxlength': 100}))
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password',)


class AskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'minlength': 1, 'maxlength': 100}))

    text = forms.CharField(widget=forms.Textarea(attrs={'minlength': 1}))

    tags = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 100}))

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags',)


class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'minlength': 1}))

    class Meta:
        model = Answer
        fields = ('text',)


class SettingsFormUser(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('email',)


class SettingsFormProfile(forms.ModelForm):
    nickname = forms.CharField(required=False, widget=forms.TextInput(attrs={'minlength': 1, 'maxlength': 50}))

    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput())

    class Meta:
        model = Profile
        fields = ('nickname',)


class SignupFormUser(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'minlength': 5,'maxlength': 50}))

    password = forms.CharField(widget=forms.PasswordInput)

    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    email = forms.EmailField(widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def clean_password_confirmation(self):
        password = self.cleaned_data['password']
        password_conf = self.cleaned_data['password_confirmation']
        if password != password_conf:
            raise forms.ValidationError("password is incorrect")
        return password_conf


class SignupFormProfile(forms.ModelForm):
    nickname = forms.CharField(widget=forms.TextInput(attrs={'minlength': 1, 'maxlength': 50}))

    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput())

    class Meta:
        model = Profile
        fields = ('nickname',)
