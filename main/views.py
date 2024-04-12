from django.shortcuts import redirect, render
from django.views import generic
from main.models import CustomUser, Document, Report
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from main.forms import ReportForm, ResolveMessageForm, EventForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from main.models import Report
from django.views.decorators.csrf import csrf_exempt
from main.s3_utils import get_s3_presigned_url
from .models import Event
from django.views.generic import TemplateView
from .models import CustomUser, Event
import requests
from .forms import EventForm  # Assuming you have an EventForm form class
from django.contrib import messages

@login_required(login_url="/accounts/login/")
def admin_view(request):
    if not request.user.is_site_admin:
        return HttpResponseForbidden(
            "You not a site admin. Please login as a site admin or request access."
        )
    reports = Report.objects.all()
    for report in reports:
        report_docs = report.document.all()
        file_urls = [get_s3_presigned_url(doc.document.name) for doc in report_docs]
        report.images = [
            url
            for url in file_urls
            if any(tag in url for tag in [".jpg", ".jpeg", ".png", ".webp", ".gif"])
        ]
        report.txts = [url for url in file_urls if ".txt" in url]
        report.pdfs = [url for url in file_urls if ".pdf" in url]

    if request.method == "POST":
        form = ResolveMessageForm(request.POST, request.FILES)
        event_form = EventForm(request.POST)

        if form.is_valid():
            notes = form.cleaned_data["admin_notes"]
            curr_report = Report.objects.get(id=request.POST.get("form_id"))
            curr_report.admin_notes = notes
            curr_report.is_in_review = False
            curr_report.is_resolved = True
            curr_report.save()

        if event_form.is_valid():
            messages.success(request, 'Event created successfully')
            event_form.save()
            event_form = EventForm()

    else:
        form = ResolveMessageForm()
        event_form = EventForm()
    return render(request, "main/admin-view.html", {"reports": reports, "form": form, "event_form": event_form})


class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.all()
        if self.request.user.is_authenticated:
            context["user"] = CustomUser.objects.get(username=self.request.user)
        return context


def eventView(request):
    events = Event.objects.all()
    return render(request, 'main/home_events.html', {'events': events})


def LogoutView(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logged out successfully"}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


def report_upload_view(request):
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            new_report = form.save(commit=False)
            # Anonymous user
            if not request.user.is_authenticated:
                new_report.user = None
            else:
                new_report.user = request.user
            new_report.save()
            return redirect(f"{new_report.id}/upload", {"files": {}, "report": new_report})
    else:
        form = ReportForm()
    return render(request, "main/report_upload.html", {"form": form})


def document_upload_view(request, report_id):
    files = request.FILES.getlist("files")
    if request.method == "POST":
        for file in files:
            doc = Document.objects.create(document=file, title=file.name)
            report = Report.objects.get(id=report_id)
            report.document.add(doc)
        return redirect("main:index")
    return render(request, "main/document_upload.html", {"files": files, "report_id": report_id})


@csrf_exempt
def document_upload(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        return document_upload_view(request, report_id)
    return JsonResponse({"status": "error"})


def user_reports(request):
    # Assuming you want to display reports for the logged-in user
    reports = Report.objects.filter(user=request.user)  # come back later
    context = {'reports': reports}
    return render(request, 'main/myreports.html', context)


# This function is used to update the is_in_review field of a report when clicked
@csrf_exempt
def update_report(request):
    report_id = request.POST.get('report_id')
    if request.method == 'POST':
        report = Report.objects.get(id=report_id)
        if not report.is_resolved:
            report.is_in_review = True
        report.save()
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error"})


@login_required(login_url="/accounts/login/")
def admin_notes(request, report_id):
    report = Report.objects.get(id=report_id)
    if request.method == "POST":
        form = ResolveMessageForm(request.POST)
        if form.is_valid():
            report.admin_notes = form.cleaned_data["admin_notes"]
            report.save()
            return redirect("main:index")
    else:
        form = ResolveMessageForm()
    return render(request, "main/admin_notes.html", {"form": form, "report": report})


def create_event(request):
    # Initialize your form
    event_form = EventForm()

    if request.method == 'POST':
        # Check if the form is submitted with the specific button
        if 'upload_button' in request.POST:
            event_form = EventForm(request.POST)
            if event_form.is_valid():
                # Process the form, e.g., save the form data
                event_form.save()
                # Redirect to the same page (or another page), which clears the form
                return redirect("admin-view")  # Use the name of your URL pattern for this view

        else:
            event_form = EventForm()

    # Render the form again for GET request or if the form is not valid
    return render(request, 'main/admin-view.html', {'event_form': event_form})


def delete_report(request, report_id):
    if request.method == 'POST':
        report = Report.objects.get(id=report_id)
        report.delete()

        reports = Report.objects.filter(user=request.user)
        context = {'reports': reports}
        return render(request, 'main/myreports.html', context)
