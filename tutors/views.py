from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Tutor
from subjects.models import Subject


SORT_OPTIONS = {
    'price_asc': 'Цена: по возрастанию',
    'price_desc': 'Цена: по убыванию',
    'experience_desc': 'Опыт: по убыванию',
    'name_asc': 'Имя: А → Я',
}


def _build_querystring(request, page=None):
    """Собирает GET-параметры для ссылок пагинации, сохраняя все фильтры."""
    params = request.GET.copy()
    if page is not None:
        params['page'] = page
    else:
        params.pop('page', None)
    return params.urlencode()


def tutor_list(request):
    # Добавили order_by('name') по умолчанию, чтобы не было UnorderedObjectListWarning
    tutors = Tutor.objects.filter(is_active=True).select_related('subject').order_by('name')
    subjects = Subject.objects.all()

    # --- Фильтры ---
    subject_slug = request.GET.get('subject', '').strip()
    price_min = request.GET.get('price_min', '').strip()
    price_max = request.GET.get('price_max', '').strip()
    experience_min = request.GET.get('experience_min', '').strip()
    q = request.GET.get('q', '').strip()

    if subject_slug:
        tutors = tutors.filter(subject__slug=subject_slug)

    if price_min.isdigit():
        tutors = tutors.filter(price__gte=int(price_min))

    if price_max.isdigit():
        tutors = tutors.filter(price__lte=int(price_max))

    if experience_min.isdigit():
        tutors = tutors.filter(experience__gte=int(experience_min))

    if q:
        tutors = tutors.filter(name__icontains=q)

    # --- Сортировка ---
    sort = request.GET.get('sort', '').strip()
    if sort == 'price_asc':
        tutors = tutors.order_by('price')
    elif sort == 'price_desc':
        tutors = tutors.order_by('-price')
    elif sort == 'experience_desc':
        tutors = tutors.order_by('-experience')
    elif sort == 'name_asc':
        tutors = tutors.order_by('name')
    else:
        sort = ''
        # Если сортировка не выбрана, уже отсортировано по имени выше

    # --- Пагинация (9 на стр.) ---
    paginator = Paginator(tutors, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    filters_querystring = _build_querystring(request, page=None)

    return render(request, 'tutors/list.html', {
        'tutors': page_obj,
        'subjects': subjects,
        'selected_subject': subject_slug,
        'price_min': price_min,
        'price_max': price_max,
        'experience_min': experience_min,
        'q': q,
        'sort': sort,
        'sort_options': SORT_OPTIONS,
        'filters_querystring': filters_querystring,
        'paginator': paginator,
    })


def tutor_detail(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    return render(request, 'tutors/detail.html', {'tutor': tutor})