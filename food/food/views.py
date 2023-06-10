from django.shortcuts import render, redirect


def not_found(request):
    return render(request, '404.html')
