from django import forms

class signup_form(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=50)
    referal = forms.CharField(max_length=24,required=False)
    
class login_form(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50)