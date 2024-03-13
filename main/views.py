from django.views import generic
from main.models import CustomUser
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from main.forms import DocumentForm
from main.models import Document
from main.s3_utils import upload_file_to_s3
from django.conf import settings


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


def document_upload_view(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_doc = form.save(commit=False)
            new_doc.user = request.user
            new_doc.save()
            return redirect("main:index")
    else:
        form = DocumentForm()
    return render(request, "main/document_upload.html", {"form": form})
