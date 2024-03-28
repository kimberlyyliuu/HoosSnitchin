# REFERENCES
# Title: Django Uploading Multiple Files
# URL: https://docs.djangoproject.com/en/5.0/topics/http/file-uploads/#uploading-multiple-files
# From: Django Documentation
# Note: The code between the "Django Uploading Multiple Files code" comment is the code snippet used.

from allauth.account.forms import SignupForm
from main.models import Report
from django import forms


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["description", "event"]


class ResolveMessageForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["admin_notes"]


# vvv Django Uploading Multiple Files code vvv
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class DocumentForm(forms.Form):
    file_field = MultipleFileField()
# ^^^ Django Uploading Multiple Files code ^^^
