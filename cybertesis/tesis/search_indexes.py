from haystack import indexes
from tesis.models import Tesis


class FullIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # tesis_year = indexes.DateTimeField(model_attr='year')
    # description = indexes.EdgeNgramField(model_attr='description')
    tesis_title = indexes.EdgeNgramField(model_attr='title')
    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(model_attr='description')

    def get_model(self):
        return Tesis

    def index_queryset(self, using=None):
        """ Cuando todo el index se actualiza """
        return self.get_model().objects.all()
