from django import forms


class NewRepository(forms.Form):
    url = forms.CharField(label="Repository Url", max_length=512)
