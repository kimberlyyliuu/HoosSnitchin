from django.shortcuts import redirect, render
from django.views import generic
from main.models import CustomUser, Event, Document, Report
from django.contrib.auth import logout, get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect
from main.forms import ReportForm, DocumentForm


# display the user's name
class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context["user"] = CustomUser.objects.get(username=self.request.user)
            return context
        else:
            return super().get_context_data(**kwargs)


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
            #Anonymous user
            if not request.user.is_authenticated:
                new_report.user = CustomUser.objects.get(username='anonymousSubmissions')
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
            
            files = form.cleaned_data['file_field']
            for f in files:
                doc = Document.objects.create(document=f)
                report = Report.objects.get(id=report_id)
                report.document.add(doc)
            
            return redirect("main:index")
    else:
        form = DocumentForm()
    return render(request, "main/document_upload.html", {"form": form})