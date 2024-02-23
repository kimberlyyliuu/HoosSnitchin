from django.views import generic
from users.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin


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
