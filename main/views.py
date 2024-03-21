from django.shortcuts import redirect, render
from django.views import generic
from main.models import CustomUser, Document, Report
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from main.forms import ReportForm, DocumentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from main.models import Report
from main.s3_utils import get_s3_presigned_url
from .models import Event
import requests


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
    return render(request, "main/admin-view.html", {"reports": reports})


class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context["user"] = CustomUser.objects.get(username=self.request.user)
            return context
        else:
            return super().get_context_data(**kwargs)

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
            return redirect(f"{new_report.id}/upload", {"report": new_report})
    else:
        form = ReportForm()
    return render(request, "main/report_upload.html", {"form": form})


def document_upload_view(request, report_id):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():

            files = form.cleaned_data["file_field"]
            for f in files:
                doc = Document.objects.create(document=f, title=f.name)
                report = Report.objects.get(id=report_id)
                report.document.add(doc)

            return redirect("main:index")
    else:
        form = DocumentForm()
    return render(request, "main/document_upload.html", {"form": form})


def user_reports(request):
    # Assuming you want to display reports for the logged-in user
    reports = Report.objects.filter(user=request.user) #come back later
    context = {'reports': reports}
    return render(request, 'main/mysnitches.html', context)


