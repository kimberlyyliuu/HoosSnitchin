from django.shortcuts import redirect, render
from django.views import generic
from main.models import CustomUser, School
from django.contrib.auth import logout, get_user_model
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
        
# Pick from list of schools
def select_school(request):
    if request.method == 'POST':
        school_id = request.POST['school']
        #print(school_id)
        request.user.school_membership = school_id
        request.user.save()

        User = get_user_model()
        request.user = User.objects.get(id=request.user.id)

        return redirect('/')
    else:
        schools = School.objects.all()
        return render(request, 'main/school_list.html', {'schools': schools})


def LogoutView(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logged out successfully"}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

