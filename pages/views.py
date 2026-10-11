from django.shortcuts import render
from tutors.models import Tutor

def index(request):
    tutors = Tutor.objects.filter(is_active=True)[:6]
    return render(request, 'index.html', {'tutors': tutors})

def about(request):
    return render(request, 'about.html')

def contacts(request):
    return render(request, 'contacts.html')