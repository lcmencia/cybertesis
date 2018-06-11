from django.conf.urls import url
from ajax import view

urlpatterns = [
    url(r'^add_rating/', view.add_rating, name='ajax_add_rating'),
]
