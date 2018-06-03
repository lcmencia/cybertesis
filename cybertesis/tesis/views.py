from django.core import serializers
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import render

from .models import Tesis, Faculty, Full, Searches, Institution


def index(request):
    tesis_list = Tesis.objects.all()
    faculty_list = Faculty.objects.all()
    university_list = Institution.objects.all()
    searches = Searches.objects.all()
    total_searchs_sum = Searches.objects.aggregate(Sum('count'))
    total_searchs = total_searchs_sum['count__sum']
    total_searchs = 0 if total_searchs is None else total_searchs
    total_tesis = len(tesis_list)
    total_faculty = len(faculty_list)
    total_institution = len(university_list)
    total_words = len(searches)
    all_full = Full.objects.all()
    last = all_full.reverse()[0]
    context = {'tesis_list': all_full, 'total_tesis': total_tesis, 'total_faculty': total_faculty,
               'init_year': last.year, 'total_institution': total_institution, 'total_words': total_words,
               'total_searchs': total_searchs}
    return render(request, "index.html", context)


def search(request):
    data = request.GET
    search = data.get('search_text', '').lower()
    total_full = list()
    if len(search) > 0:
        all_full = Full.objects.all()
        for full in all_full:
            for i in range(0, len(full._meta.fields)):
                key = full._meta.fields[i].attname
                value = str(full.__getattribute__(key)).lower()
                if search in value:
                    total_full.append(full)
                    break

        obj, created = Searches.objects.update_or_create(word=search)
        if not created:
            obj.count += 1
        else:
            if obj.count is None:
                obj.count = 1
        obj.save()

    the_data = serializers.serialize("json", [x for x in total_full])
    return HttpResponse(the_data, content_type='application/json')
