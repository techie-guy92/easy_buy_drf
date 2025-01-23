from django import forms
from .models import CustomUser
from utilities import *


#======================================= Custom User Form ====================================

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput(render_value=True))
    re_password = forms.CharField(label="Re_Password", widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "user_type"]

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if first_name:
            cleaned_data["first_name"] = first_name.capitalize()
        if last_name:
            cleaned_data["last_name"] = last_name.capitalize()
        return cleaned_data

    def clean_re_password(self):
        pass1 = self.cleaned_data.get("password")
        pass2 = self.cleaned_data.get("re_password")
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("رمز عبور و تکرار آن یکسان نمی باشد.")
        return pass2

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not passwordRe.match(password):
            raise forms.ValidationError("رمز عبور باید متشکل از حروف کوچک، بزرگ و عدد باشد و همچنین هشت رقم داشته باشد.")
        return password

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not emailRe.match(email):
            raise forms.ValidationError("ایمیل معتبر نیست.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "user"
        user.set_password(self.cleaned_data["password"])
        user.username = f"{user.first_name.lower()}_{user.last_name.lower()}"
        if commit:
            user.save()
        return user

        
#=============================================================================================