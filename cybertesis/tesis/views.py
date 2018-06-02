from django.shortcuts import render


def index(request):
    context = {'name': 'value'}
    return render(request, "index.html", context)


def search(request):
    q = request.GET.get('search_text', '')
    #university = SearchQuerySet().models(Univer).filter(content=q)
    #the_data = serializers.serialize("json", [x.object for x in profession])
    #return HttpResponse(the_data, content_type='application/json')