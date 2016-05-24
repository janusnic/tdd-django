from django.conf import settings

from django.db.models import Q
from django.http import QueryDict
from photo.models import Photo

def get_search_queryset(query):
    """
    Build and return a Photo queryset based on the parameters passed in, which will be a querystring
    containing the user's search terms.
    """
    data = QueryDict(query)
    queryset = Photo.objects.all()

    q = data.get('q')
    a = data.getlist('a')
    p = data.getlist('p')
    l = data.getlist('l')

    if q:
        queryset = queryset.filter(Q(name__icontains=q) | Q(album__name__icontains=q))
    if a:
        queryset = queryset.filter(album__in=a)
    if p:
        queryset = queryset.filter(people__in=p)
    if l:
        queryset = queryset.filter(album__location__in=l)

    return queryset