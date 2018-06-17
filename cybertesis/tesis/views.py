import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from whoosh.analysis import StopFilter, LanguageAnalyzer, StemFilter

from services.searches import SearchesServices
from services.tesis import TesisServices
from services.resume import ResumeServices

from django.contrib.auth import authenticate, login

from tesis import constants
from .constants import ORDER_BY_MOST_RECENT
from .models import Searches, Category, Tesis, Faculty, Career, Full, SubCategory, Person


def authentication(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/dashboard')
    else:
        return render(request, 'login.html', {})


@login_required()
@require_http_methods(['GET'])
def dashboard(request):
    if not request.user.is_authenticated or request.user.dataentry.institution == None:
        return redirect('/login')

    institution_id = request.user.dataentry.institution.id
    full_list = Full.objects.filter(institution_id=institution_id)

    return render(request, 'dashboard.html', {'tesis_list': full_list})


@login_required()
@require_http_methods(['GET', 'POST'])
def add_tesis(request):
    if not request.user.is_authenticated or request.user.dataentry.institution == None:
        return redirect('/login')

    method = request.method
    institution_id = request.user.dataentry.institution.id

    faculty_list = Faculty.objects.filter(institution__id=institution_id)
    faculty_list_parsed = list()
    career_list_parsed = list()
    subcategory_list_parsed = list()
    faculty_id_list = list()
    for faculty in faculty_list:
        item = {'id': faculty.id, 'name': faculty.name}
        faculty_list_parsed.append(item)
        faculty_id_list.append(faculty.id)

    career_list = Career.objects.filter(faculty_id__in=faculty_id_list)
    for career in career_list:
        item = {'id': career.id, 'name': career.name, 'fk': career.faculty.id}
        career_list_parsed.append(item)

    subcategory_list = SubCategory.objects.all()
    for sub in subcategory_list:
        item = {'id': sub.id, 'name': sub.sub_category_name}
        subcategory_list_parsed.append(item)

    if method == 'GET':
        return render(request, 'add_tesis.html',
                      {'faculty_list': json.dumps(faculty_list_parsed), 'career_list': json.dumps(career_list_parsed),
                       'subcategory_list': json.dumps(subcategory_list_parsed), 'types': constants.TYPE_CHOICES})

    elif method == 'POST':
        data = request.POST
        title = data.get('title', '')
        faculty = data.get('faculty', '')
        career = data.get('career', '')
        year = data.get('year', '')
        subcategories = data.getlist('subcategory')
        resume = data.get('resume', '')
        link = data.get('link', '')
        format = data.get('format', '')
        authors = data.get('authors', '')
        tutor1 = data.get('tutor1', '')
        tutor2 = data.get('tutor2', '')
        type = data.get('type', '')
        messages = list()
        if title is None or len(title) == 0:
            messages.append({'tags': 'alert-danger', 'text': 'Ingrese el título'})
        if resume is None or len(resume) == 0:
            if len(messages) == 0:
                messages.append({'tags': 'alert-danger', 'text': 'Ingrese el resumen'})
        if year is None or len(year) == 0:
            if len(messages) == 0:
                messages.append({'tags': 'alert-danger', 'text': 'Ingrese el año'})
        if subcategories is None or len(subcategories) == 0:
            if len(messages) == 0:
                messages.append({'tags': 'alert-danger', 'text': 'Seleccione al menos una subcategoria'})
        if authors is None or len(authors) == 0:
            if len(messages) == 0:
                messages.append({'tags': 'alert-danger', 'text': 'Ingrese el/los autor/es'})
        if (tutor1 is None or len(tutor1) == 0) and (tutor2 is None or len(tutor2) == 0):
            if len(messages) == 0:
                messages.append({'tags': 'alert-danger', 'text': 'Ingrese el/los tutor/es'})

        if len(messages) == 0:
            new_tesis = Tesis()
            new_tesis.title = title
            new_tesis.description = resume
            new_tesis.tesis_type = type
            new_tesis.url = link
            new_tesis.format = format
            new_tesis.year = year
            new_tesis.career = Career.objects.get(pk=career)
            new_tesis.save()

            authors_checked = authors.split(",")
            for a in authors_checked:
                obj, created = Person.objects.update_or_create(name=a)
                new_tesis.author.add(obj)
            if not (tutor1 is None or len(tutor1) == 0):
                obj, created = Person.objects.update_or_create(name=tutor1)
                new_tesis.tutor.add(obj)
            if not (tutor2 is None or len(tutor2) == 0):
                obj, created = Person.objects.update_or_create(name=tutor2)
                new_tesis.tutor.add(obj)
            for s in subcategories:
                new_tesis.sub_category.add(SubCategory.objects.get(pk=s))
            new_tesis.save()
            messages.append({'tags': 'alert-success', 'text': 'Tesis creada'})
            return render(request, 'add_tesis.html',
                          {'faculty_list': json.dumps(faculty_list_parsed),
                           'career_list': json.dumps(career_list_parsed), 'messages': messages,
                           'subcategory_list': json.dumps(subcategory_list_parsed), 'types': constants.TYPE_CHOICES})

        return render(request, 'add_tesis.html',
                      {'faculty_list': json.dumps(faculty_list_parsed), 'career_list': json.dumps(career_list_parsed),
                       'subcategory_list': json.dumps(subcategory_list_parsed), 'types': constants.TYPE_CHOICES,
                       'messages': messages, 'format': format, 'title': title, 'faculty': faculty, 'career': career,
                       'year': year, 'authors': authors, 'link': link, 'subcategories': json.dumps(subcategories),
                       'resume': resume, 'tutor1': tutor1, 'tutor2': tutor2, 'type': type})


@require_http_methods(['GET'])
def index(request):
    data = request.GET
    question = data.get('q', None)
    category_selected = 0
    category_name = ''

    # Top de categorias
    tesis_services = TesisServices()
    tesis_services.generate_tesis_resume()
    tesis_top_categories = tesis_services.top_categories

    # Top tutores
    recommended_tutors = tesis_services.top_tutors

    if len(data) > 0:
        category_selected = data.get('category_id', 0)
        category_selected = int(category_selected)
        if category_selected > 0:
            # La pagina esta siendo filtrada por una categoria
            category = Category.objects.get(pk=category_selected)
            category_name = category.category_name

    # Todas las tesis a mostrarse, ordenado de mas reciente a menos
    if question:
        all_full = tesis_services.get_by_category(0, ORDER_BY_MOST_RECENT)
        all_full, recommended_tutors = TesisServices.search_in_tesis(question, all_full)
    else:
        all_full = tesis_services.get_by_category(category_selected, ORDER_BY_MOST_RECENT)

    ################ Seccion resumen (4 cuadraditos) ################
    resume_service = ResumeServices()
    resume_service.generate_resume()
    searches_services = SearchesServices()
    searches_services.generate_resume()
    ###### Cuadradito 1 ######
    total_tesis = resume_service.total_tesis_number
    init_year = resume_service.init_year
    ###### Cuadradito 2 ######
    # Total de universidades en el sitio
    total_institution = resume_service.total_institution
    # Total de facultades en el sitio
    total_faculty = resume_service.total_faculty
    ###### Cuadradito 3 ######
    # Porcentaje de tesis presentadas en el interior con respecto al total de tesis del pais
    outside_capital_percentage = resume_service.outside_capital_percentage
    # En la lista de tesis se evaluan la cantidad que hubo en cada año en el interior los ultimos 2 años para saber la tendencia
    trending = resume_service.trending
    ###### Cuadradito 4 ######
    # Total de palabras diferentes
    total_words = searches_services.total_words
    # Total de busquedas en el sitio
    total_searchs = searches_services.total_searchs

    ################ Seccion Top Tutores y Busquedas ################
    # Top de busquedas
    top_words_searched = searches_services.top_words_searched

    # Paginado de lista de tesis
    paginator = Paginator(all_full, 5)
    page = request.GET.get('page')
    tesis_list = paginator.get_page(page)
    context = {
        # C1
        'total_tesis': total_tesis, 'init_year': init_year,
        # C2
        'total_faculty': total_faculty, 'total_institution': total_institution,
        # C3
        'outside_capital_percentage': outside_capital_percentage, 'trending': trending,
        # C4
        'total_searchs': total_searchs, 'total_words': total_words,
        # Tabla busquedas
        'top_words_searched': top_words_searched,
        # Tabla tesis
        'tesis_list': tesis_list,
        # Top categorias de la izquierda
        'tesis_top_categories': tesis_top_categories,
        # Filtro de categoria
        'category_name': category_name, 'category_selected': category_selected,
        # Tutores recomendados
        'recommended_tutors': recommended_tutors,
        # Pregunta buscada, para el caso de paginación
        'question':question
    }
    return render(request, "index.html", context)


@require_http_methods(['GET'])
def search(request):
    data = request.GET
    category_id = int(data.get('category_id', 0))
    order = int(data.get('order', ORDER_BY_MOST_RECENT))
    search_text = data.get('search_text', '').lower()
    tesis_services = TesisServices()
    total_full = list()
    tutors_full = list()
    all_full = tesis_services.get_by_category(category_id, order)

    if len(search_text) > 0:
        total_full, tutors_full = TesisServices.search_in_tesis(search_text, all_full)

        # Por cada busqueda, en la tabla de palabras buscadas, si la palabra existe se suma 1, sino se inserta con valor 1
        # Si lo que se ingresa como búsqueda no es una sola pabla, sino una frase, se utiliza filtros tipo Stop y Stemming,
        # luego se realiza la extracción de keywords o tokens
        """
        “Stop” words are words that are so common it’s often counter-productive to index them, such as “and”, 
        “or”, “if”, etc. The provided analysis.StopFilter lets you filter out stop words, and includes a default 
        list of common stop words.
        Stemming is a heuristic process of removing suffixes (and sometimes prefixes) from words to arrive (hopefully, 
        most of the time) at the base word.
        """
        if len(search_text.split()) > 1:
            analyzer = LanguageAnalyzer("es")
            a_filters = StopFilter() | StemFilter()
            keywords = list(set([token.text for token in a_filters(analyzer(search_text, no_morph=True))]))
        else:
            keywords = [search_text]

        for word in keywords:
            obj, created = Searches.objects.update_or_create(word=word)
            if not created:
                obj.count += 1
            else:
                if obj.count is None:
                    obj.count = 1
            obj.save()
    else:
        total_full = all_full

    # Se actualiza las palabras más buscadas
    # Se actualiza total de búsquedas y cantidad de palabras diferentes
    searches_services = SearchesServices()
    searches_services.generate_resume()
    top_words_searched = searches_services.top_words_searched
    # Total de palabras diferentes
    total_words = searches_services.total_words
    # Total de busquedas en el sitio
    total_searchs = searches_services.total_searchs

    # Paginado de lista de tesis
    paginator = Paginator(total_full, 5)
    page = request.GET.get('page')
    tesis_list = paginator.get_page(page)
    the_data = {'tesis_list': render_to_string('sections/central_published_tesis.html', {'tesis_list': tesis_list,
                                                                                         'question': search_text}),#serializers.serialize("json", [x for x in total_full]),
                'tutors_list': tutors_full,
                'top_words_searched': top_words_searched,
                'total_words': total_words,
                'total_searchs': total_searchs,
                'question': search_text
                }
    # the_data = serializers.serialize("json", [x for x in total_full])
    return JsonResponse(the_data)


@require_http_methods(['GET'])
def tesis(request, tesis_id=None):
    tesis_data = {}
    if tesis_id:
        tesis_data = TesisServices.get_by_id(tesis_id)

    if tesis_data:
        context = {'tesis': tesis_data}
        return render(request, "tesis-resume.html", context)
    else:
        messages.error(request, 'No se ha encontrado una tesis para el ID correspondiente')
        return redirect('index')
