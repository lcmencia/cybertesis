from django.contrib import messages
from django.core import serializers
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from services.faculty import FacultyService
from services.searches import SearchesServices
from services.tesis import TesisServices

from .models import Tesis, Faculty, Full, Searches, Institution


def index(request):
    tesis_services = TesisServices()
    tesis_services.generate_tesis_resume()
    university_list = Institution.objects.all()
    searches = Searches.objects.all()
    facultyu_info = FacultyService()
    facultyu_info.get_all_faculty_info()

    # Top de categorias
    tesis_top_categories = tesis_services.top_categories

    # Top de busquedas
    top_words_searched = SearchesServices().get_top_words_searched()

    # Total de busquedas en el sitio
    total_searchs_sum = Searches.objects.aggregate(Sum('count'))
    total_searchs = total_searchs_sum['count__sum']
    total_searchs = 0 if total_searchs is None else total_searchs

    # Total de universidades en el sitio
    total_institution = len(university_list)

    # Total de tesis en el sitio
    total_tesis = tesis_services.total_tesis

    # Total de facultades en el sitio
    total_faculty = facultyu_info.total_tesis

    # Total de palabras diferentes
    total_words = len(searches)

    # Todas las tesis a mostrarse, ordenado de mas reciente a menos
    all_full = Full.objects.all().order_by('-year', '-added_date')

    # Se obtiene la primera tesis, la ultima de la lista, para sacar el dato desde que año tenemos tesis
    last = all_full.reverse()[0]
    init_year = last.year

    # Porcentaje de tesis presentadas en el interior con respecto al total de tesis del pais
    outside_capital_percentage = facultyu_info.outside_capital_percentage

    context = {'tesis_list': all_full, 'total_tesis': total_tesis, 'total_faculty': total_faculty,
               'init_year': init_year, 'total_institution': total_institution, 'total_words': total_words,
               'total_searchs': total_searchs, 'outside_capital_percentage': outside_capital_percentage,
               'top_words_searched': top_words_searched, 'tesis_top_categories': tesis_top_categories}
    return render(request, "index.html", context)


def search(request):
    data = request.GET
    search = data.get('search_text', '').lower()
    total_full = list()
    if len(search) > 0:
        # Cuando se realiza una busqueda obtenemos todas las tesis
        all_full = Full.objects.all()
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

    the_data = serializers.serialize("json", [x for x in total_full])
    return HttpResponse(the_data, content_type='application/json')


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
