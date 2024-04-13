from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from main.forms import EventForm, ReportForm, ResolveMessageForm
from main.models import CustomUser, Document, Event, Report
from main.s3_utils import get_s3_presigned_url


# vvvvvvvvvvvv Index View vvvvvvvvvvvv
class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.all()
        if self.request.user.is_authenticated:
            context["user"] = CustomUser.objects.get(username=self.request.user)
        return context


# vvvvvvvvvvvv Admin View vvvvvvvvvvvv
@login_required(login_url="/accounts/login/")
def admin_view(request):
    if not request.user.is_site_admin:
        return HttpResponseForbidden(
            "You not a site admin. Please login as a site admin or request access."
        )
    reports = Report.objects.all().order_by("-is_in_review", "-date_time")
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
        resolve_form = ResolveMessageForm(request.POST, request.FILES)
        event_form = EventForm(request.POST)

        if resolve_form.is_valid():
            notes = resolve_form.cleaned_data["admin_notes"]
            curr_report = Report.objects.get(id=request.POST.get("form_id"))
            curr_report.admin_notes = notes
            curr_report.is_in_review = False
            curr_report.is_resolved = True
            curr_report.save()

        if event_form.is_valid():
            messages.success(request, "Event created successfully")
            event_form.save()
            event_form = EventForm()

    else:
        resolve_form = ResolveMessageForm()
        event_form = EventForm()
    return render(
        request,
        "main/admin_view.html",
        {"reports": reports, "resolve_form": resolve_form, "event_form": event_form},
    )


# [TODO: Come back here and see what we can do to not make this javascript lol]
@csrf_exempt
def update_report(request):
    report_id = request.POST.get("report_id")
    if request.method == "POST":
        report = Report.objects.get(id=report_id)
        if not report.is_resolved:
            report.is_in_review = True
        report.save()
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error"})


# vvvvvvvvvvvv Report / Document Uploading vvvvvvvvvvvv
def report_upload_view(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            new_report = form.save(commit=False)
            if not request.user.is_authenticated:
                new_report.user = None
            else:
                new_report.user = request.user
            new_report.event = event
            new_report.save()
            return redirect("main:document_upload", report_id=new_report.id)
    else:
        form = ReportForm()
    return render(request, "main/report_upload.html", {"form": form, "event": event})


def document_upload_view(request, report_id):
    if request.method == "POST":
        files = request.FILES.getlist("files")
        for file in files:
            doc = Document.objects.create(document=file, title=file.name)
            report = Report.objects.get(id=report_id)
            report.document.add(doc)
        return redirect("main:index")
    return render(request, "main/document_upload.html", {"report_id": report_id})


# vvvvvvvvvvvv User Report Management vvvvvvvvvvvv
def my_reports(request):
    reports = Report.objects.filter(user=request.user)  # come back later
    context = {"reports": reports}
    return render(request, "main/my_reports.html", context)


def delete_report(request, report_id):
    if request.method == "POST":
        report = Report.objects.get(id=report_id)
        report.delete()

        reports = Report.objects.filter(user=request.user)
        context = {"reports": reports}
        return render(request, "main/my_reports.html", context)
