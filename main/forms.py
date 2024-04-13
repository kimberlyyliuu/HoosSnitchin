from main.models import Report
from main.models import Event
from django import forms


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
