from django.shortcuts import render
from .models import Subject

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/list.html', {'subjects': subjects})