from django.shortcuts import render

# Create your views here.
def homePage(request):
    context = {}
    return render(request, "mainApp/homePage.html", context)
