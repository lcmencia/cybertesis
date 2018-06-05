from tesis.models import Searches


class SearchesServices:

    def __init__(self):
        # Limite de palabras más búscadas
        self.LIMIT = 5

    def get_top_words_searched(self):
        """ Retorna una lista de palabras más buscadas con su cantidad correspondiente, como un diccionario, y
        ordenado de mayor a menor, se utiliza un límite de tamñano de lista a retornar """

        searches = Searches.objects.all()
        searches_list = [{'word': word.word, 'count': word.count} for word in searches.all()]
        return sorted(searches_list, key=lambda k: k['count'], reverse=True)[:self.LIMIT]
