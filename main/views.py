from django.views import generic
from main.models import CustomUser
from django.contrib.auth import logout
from django.http import JsonResponse


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
