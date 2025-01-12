from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import PasswordInput
from re import compile
from .models import CustomUser


#======================================= Custom User Form ====================================

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput(render_value=True))
    re_password = forms.CharField(label="Re_Password", widget=forms.PasswordInput(render_value=True))
    
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "user_type",]
        
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
                raise ValidationError("رمز عبور و تکرار آن یکسان نمی باشد.")
            return pass2
        
        def clean_password(self):
            passwordRe = compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*]).{8,}$")
            password = self.cleaned_data["password"]
            if not passwordRe.match(password):
                raise ValidationError("رمز عبور باید متشکل از حروف کوچک، بزرگ و عدد باشد و همچنین هشت رقم داشته باشد.")
            return password
        
        def clean_email(self):
            emailRe = compile(r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$")
            email = self.cleaned_data["email"]
            if not emailRe.match(email):
                raise ValidationError("ایمیل معتبر نیست.")
            return email

        def save(self, commit=True):
            user = super().save(commit=False)
            user.user_type = "user"
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            return user
        

#=============================================================================================