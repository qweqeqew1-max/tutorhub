from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Tutor
from subjects.models import Subject

def tutor_list(request):
    tutors = Tutor.objects.filter(is_active=True)
    subjects = Subject.objects.all()

    subject_slug = request.GET.get('subject')
    if subject_slug:
        tutors = tutors.filter(subject__slug=subject_slug)

    paginator = Paginator(tutors, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tutors/list.html', {
        'tutors': page_obj,
        'subjects': subjects,
        'selected_subject': subject_slug,
    })


def tutor_detail(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    return render(request, 'tutors/detail.html', {'tutor': tutor})