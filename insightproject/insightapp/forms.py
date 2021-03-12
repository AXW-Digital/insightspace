from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


#login
class LoginForm(forms.Form):
    """class creates our login form"""
    email = forms.EmailField(label="email address")
    password = forms.CharField(widget=forms.PasswordInput)


#verification
class VerifyForm(forms.Form):
    """form handles our verification"""
    key = forms.EmailField(label='please enter your email here')


class RegisterForm(forms.Form):
    """ our registration form"""
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)


    def clean_email(self):
        """method checks if we have same email with a user"""

        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('email address is taken')
        return email

    def clean_password2(self):
        """method checks that both passwords are a match"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("passwords dont match")
        return password2



class SetPasswordForm(forms.Form):
    """for reseting passwords"""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)


#for updating users
class UserAdminChangeForm(forms.ModelForm):
    """custom form for updating an already existing user"""

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin','fname', 'lname') 
    
    def clean_password(self):
        return self.initial["password"]


#
class UserAdminCreationForm(forms.ModelForm):
    """creates a new user"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        """to compare our passwords"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


    def save(self, commit=True):
        """save the password if it passes our test"""
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


