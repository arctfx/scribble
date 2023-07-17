from django.shortcuts import render


def index(request):
    return render(request, "index.html")


"""
def create_room():
    room = Room()
    # room.save()
    return render(room.__str__(), "")
"""
