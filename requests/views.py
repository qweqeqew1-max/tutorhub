from django.shortcuts import render, redirect
from .models import Request
from subjects.models import Subject
from tutors.models import Tutor

def request_create(request):
    subjects = Subject.objects.all()
    tutors = Tutor.objects.filter(is_active=True)

    if request.method == 'POST':
        Request.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            subject_id=request.POST.get('subject'),
            tutor_id=request.POST.get('tutor') or None,
            date=request.POST.get('date'),
        )
        return redirect('requests:success')

    return render(request, 'requests/form.html', {
        'subjects': subjects,
        'tutors': tutors,
    })


def request_success(request):
    return render(request, 'requests/success.html')