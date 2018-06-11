from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from services.searches import SearchesServices
from services.tesis import TesisServices
from services.resume import ResumeServices

from .constants import ORDER_BY_MOST_RECENT
from .models import Searches, Category


@require_http_methods(['GET'])
def index(request):
    data = request.GET
    category_selected = 0
    category_name = ''

    # Top de categorias
    tesis_services = TesisServices()
    tesis_services.generate_tesis_resume()
    tesis_top_categories = tesis_services.top_categories

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
        'total_tesis': total_tesis, 'init_year': init_year,
        'total_faculty': total_faculty, 'total_institution': total_institution,
        'outside_capital_percentage': outside_capital_percentage, 'trending': trending,
        'total_searchs': total_searchs, 'total_words': total_words,
        'top_words_searched': top_words_searched,
        'tesis_list': all_full,
        'tesis_top_categories': tesis_top_categories,
        'category_name': category_name, 'category_selected': category_selected}
    return render(request, "index.html", context)


@require_http_methods(['GET'])
def search(request):
    data = request.GET
    category_id = int(data.get('category_id', 0))
    order = int(data.get('order', ORDER_BY_MOST_RECENT))
    search = data.get('search_text', '').lower()
    tesis_services = TesisServices()
    total_full = list()
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
                    break

        # Por cada busqueda, en la tabla de palabras buscadas, si la palabra existe se suma 1, sino se inserta con valor 1
        obj, created = Searches.objects.update_or_create(word=search)
        if not created:
            obj.count += 1
        else:
            if obj.count is None:
                obj.count = 1
        obj.save()
    else:
        total_full = all_full

    the_data = serializers.serialize("json", [x for x in total_full])
    return HttpResponse(the_data, content_type='application/json')


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
