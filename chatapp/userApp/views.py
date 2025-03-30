from django.shortcuts import render, redirect
from .forms import RawSignInForm
from .models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

from .models import User
def profilePage(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("homePage")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        if "logout" in request.POST:
            user.active_now = False
            user.save()
            update_last_online(request)
            request.session.pop("user_id")
            return redirect('signInPage')

    context = {
        "user": user
    }
    return render(request, "userApp/profilePage.html", context)

def signInPage(request):
    my_form = RawSignInForm()

    if request.method == "POST":
        my_form = RawSignInForm(request.POST)

        if my_form.is_valid():
            email = my_form.cleaned_data['email']
            password = my_form.cleaned_data['password']

            user = User.objects.filter(email=email).first()  # Evită eroarea de obiect inexistent
            if user and password == user.password:
                print("Logare cinstita")
                # request.session['user_email'] = email
                # if user.last_time_online is None:
                #     return redirect('resetPassword')
                request.session['user_id'] =  user.id
                user.active_now = True
                user.save()
                return redirect("profilePage")
            else:
                print("Email sau parolă incorectă")
    context = {
        'form': my_form
    }
    return render(request, "userApp/signInPage.html", context)

@csrf_exempt
def update_last_online(request):
    """Actualizează last_time_online la ieșirea utilizatorului"""
    user_id = request.session.get('user_id')

    if not user_id:  # Dacă sesiunea nu există, nu face nimic
        return JsonResponse({"status": "session expired"}, status=403)

    try:
        user = User.objects.get(id=user_id)
        user.last_time_online = datetime.datetime.now()
        user.save()
        return JsonResponse({"status": "success"})
    except User.DoesNotExist:
        return JsonResponse({"status": "error"}, status=404)
