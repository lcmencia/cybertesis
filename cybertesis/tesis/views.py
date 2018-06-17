from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from whoosh.analysis import StopFilter, LanguageAnalyzer, StemFilter

from services.searches import SearchesServices
from services.tesis import TesisServices
from services.resume import ResumeServices

from django.contrib.auth import authenticate, login

from .constants import ORDER_BY_MOST_RECENT
from .models import Searches, Category, Tesis, Faculty, Career, Full


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
    #tesis_list = serializers.serialize("json", [x for x in full_list])

    # faculty_list = Faculty.objects.filter(institution__id=institution_id)
    # faculty_id_list = list()
    # for faculty in faculty_list:
    #     faculty_id_list.append(faculty.id)
    #
    # career_list = Career.objects.filter(faculty_id__in=faculty_id_list)
    # career_id_list = list()
    # for career in career_list:
    #     career_id_list.append(career.id)
    #
    # request.session['faculty_list'] = serializers.serialize("json", [y for y in faculty_list])
    # request.session['career_list'] = serializers.serialize("json", [x for x in career_list])

    return render(request, 'dashboard.html', {'tesis_list': full_list})


@require_http_methods(['GET'])
def index(request):
    data = request.GET
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
        'tesis_list': all_full,
        # Top categorias de la izquierda
        'tesis_top_categories': tesis_top_categories,
        # Filtro de categoria
        'category_name': category_name, 'category_selected': category_selected,
        # Tutores recomendados
        'recommended_tutors': recommended_tutors}
    return render(request, "index.html", context)


@require_http_methods(['GET'])
def search(request):
    data = request.GET
    category_id = int(data.get('category_id', 0))
    order = int(data.get('order', ORDER_BY_MOST_RECENT))
    search = data.get('search_text', '').lower()
    tesis_services = TesisServices()
    total_full = list()
    tutors_full = list()
    all_full = tesis_services.get_by_category(category_id, order)

    if len(search) > 0:
        for full in all_full:
            # Por cada tesis se iteran sus columnas para ver si la palabra existe
            # Esto puede ser demasiado costoso, por eso la vista de donde se obtienen las tesis
            # no tiene todas las columnas, solo las que podrian ser de interes ej: nombre, facultad, año y otros
            for i in range(0, len(full._meta.fields)):
                key = full._meta.fields[i].attname
                value = str(full.__getattribute__(key)).lower()
                # Si la palabra existe se agrega en los resultados
                if search in value:
                    total_full.append(full)
                    full_tesis = Tesis.objects.get(pk=full.id)
                    tutors_name_list = []
                    for ft_sc in full_tesis.sub_category.all():
                        # Teniendo las sub-categorías se puede llegar a los tutores de cada tesis
                        for sc_tesis in ft_sc.tesis_set.all():
                            tutors_name_list, tutors = TesisServices.generate_tutor_json_list(
                                tutors_name_list=tutors_name_list,
                                tutors_obj=sc_tesis.tutor.all(),
                                subcategy_obj=ft_sc)
                            tutors_full += tutors
                    break

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
        if len(search.split()) > 1:
            analyzer = LanguageAnalyzer("es")
            a_filters = StopFilter() | StemFilter()
            keywords = list(set([token.text for token in a_filters(analyzer(search, no_morph=True))]))
        else:
            keywords = [search]

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

    the_data = {'tesis_list': serializers.serialize("json", [x for x in total_full]),
                'tutors_list': tutors_full,
                'top_words_searched': top_words_searched,
                'total_words': total_words,
                'total_searchs': total_searchs
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
