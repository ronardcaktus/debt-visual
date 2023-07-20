from django.shortcuts import render


def home(request):
    return render(request, "country/index.html", {})
