from django.shortcuts import render
from django.utils.crypto import get_random_string


def index(request):
    return render(request, "index.html")


def create_room():
    unique_id = get_random_string(length=8)
    return render(unique_id, "")
