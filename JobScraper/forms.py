from django import forms

class AccountForm(forms.Form):
    firstName = forms.CharField(label = "First Name",  max_length=100)
    lastName = forms.CharField(label = "Last Name",  max_length=100)
    username = forms.CharField(label = "Username",  max_length=100)
    password = forms.CharField(label = "Password",  max_length=100)
    email = forms.CharField(label = "E-mail",  max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(label = "Username",  max_length=100)
    password = forms.CharField(label = "Password",  max_length=100)

class SearchForm(forms.Form):
    term = forms.CharField(label = "Term",  max_length=100)
    page = forms.CharField(label = "page",  max_length=100)
    location = forms.CharField(label = "location",  max_length=100)
    jobType = forms.CharField(label = "jobType",  max_length=100)

class JoblistingForm(forms.Form):
    title = forms.CharField(label = "title",  max_length=100)
    location = forms.CharField(label = "location",  max_length=100)
    source = forms.CharField(label = "source",  max_length=100)
    link = forms.CharField(label = "link",  max_length=100)
    

class CustomListingForm(forms.Form):
    title = forms.CharField(label = "title",  max_length=100)
    location = forms.CharField(label = "locaiton",  max_length=100)
    source = forms.CharField(label = "source",  max_length=100)
    link = forms.CharField(label = "link",  max_length=100)
    list = forms.CharField(label = "list",  max_length=100)
