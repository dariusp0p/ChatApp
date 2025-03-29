from django.shortcuts import render

from .models import User
def profilePage(request):
    users = User.objects.all()
    context = {
        "users": users
    }
    return render(request, "userApp/profilePage.html", context)
