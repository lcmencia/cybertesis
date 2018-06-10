from tesis.models import Searches
from django.db.models import Sum


class SearchesServices:

    def __init__(self):
        # Limite de palabras más búscadas
        self.LIMIT = 5
        self.total_words = 0
        self.total_searchs = 0
        self.top_words_searched = list()

    def generate_resume(self):
        searches = Searches.objects.all()
        # Total de palabras diferentes
        self.total_words = len(searches)
        # Total de busquedas en el sitio
        total_searchs_sum = Searches.objects.aggregate(Sum('count'))
        total_searchs = total_searchs_sum['count__sum']
        self.total_searchs = 0 if total_searchs is None else total_searchs
        # Lista de palabras más buscadas con su cantidad correspondiente, como un diccionario, y
        # ordenado de mayor a menor, se utiliza un límite de tamñano de lista a retornar
        searches = Searches.objects.all()
        searches_list = [{'word': word.word, 'count': word.count} for word in searches.all()]
        self.top_words_searched = sorted(searches_list, key=lambda k: k['count'], reverse=True)[:self.LIMIT]
