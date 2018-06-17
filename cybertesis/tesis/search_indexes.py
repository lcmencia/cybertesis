from haystack import indexes
from tesis.models import Full


class FullIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    tesis_title = indexes.EdgeNgramField(model_attr='title')
    cats_id = indexes.EdgeNgramField(model_attr='cats_id')
    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(model_attr='description')

    def get_model(self):
        return Full

    def index_queryset(self, using=None):
        """ Cuando el index completo se actualiza """
        return self.get_model().objects.all()
