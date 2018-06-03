from django.shortcuts import render
from django.views.generic import ListView
from .models import Tesis


def index(request):
    data = request.GET

    search = data.get('tesis_search')

    tesis_list = Tesis.objects.all()

    context = {'tesis_list': tesis_list}
    return render(request, "index.html", context)


def search(request):
    q = request.GET.get('search_text', '')
    #university = SearchQuerySet().models(Univer).filter(content=q)
    #the_data = serializers.serialize("json", [x.object for x in profession])
    #return HttpResponse(the_data, content_type='application/json')