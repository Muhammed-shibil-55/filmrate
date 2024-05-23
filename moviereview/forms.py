from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from moviereview.models import Review


class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class ReviewForm(forms.ModelForm):
    class Meta:
        fields=["title","text","rating"]
        model=Review
        labels={
            "text":"Review"
        }
        widgets={
            "text":forms.Textarea(attrs={"cols":50,"rows":3,"class":"form-control"}),
            "rating":forms.Select(attrs={"class":"form-select"}),
            "title":forms.TextInput(attrs={"class":"form-control"}),
        }
