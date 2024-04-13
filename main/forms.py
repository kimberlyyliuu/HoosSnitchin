from allauth.account.forms import SignupForm
from main.models import Report
from main.models import Event
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
        fields = ["description"]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description"]


class ResolveMessageForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["admin_notes"]
