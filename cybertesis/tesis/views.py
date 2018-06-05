from django.core import serializers
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import render
from services.faculty import FacultyService
from services.searches import SearchesServices

from .models import Tesis, Faculty, Full, Searches, Institution


def index(request):
    tesis_list = Tesis.objects.all()

    # Se buscan todas las facultades
    facultyu_info = FacultyService()
    facultyu_info.get_all_faculty_info()

    # Se extrae las palabras más buscadas
    top_words_searched = SearchesServices().get_top_words_searched()

    university_list = Institution.objects.all()
    searches = Searches.objects.all()
    total_searchs_sum = Searches.objects.aggregate(Sum('count'))
    total_searchs = total_searchs_sum['count__sum']
    total_searchs = 0 if total_searchs is None else total_searchs
    total_tesis = len(tesis_list)

    total_institution = len(university_list)
    total_words = len(searches)
    all_full = Full.objects.all()
    last = all_full.reverse()[0]
    context = {'tesis_list': all_full, 'total_tesis': total_tesis, 'total_faculty': facultyu_info.total_tesis,
               'init_year': last.year, 'total_institution': total_institution, 'total_words': total_words,
               'total_searchs': total_searchs, 'outside_capital_percentage': facultyu_info.outside_capital_percentage,
               'top_words_searched': top_words_searched}
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
