from django.conf import settings
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView
from photo.models import Album, Location
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy

class List(ListView):
    model = Album
    paginate_by = settings.PHOTOS_PER_PAGE
    template_name = 'photo/album_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Albums')
        return context

list = List.as_view()

class Detail(ListView):
    paginate_by = settings.PHOTOS_PER_PAGE

    template_name = 'photo/photo_list.html'

    def get_album(self):
        return get_object_or_404(Album, pk=self.kwargs['pk'])

    def get_queryset(self):
        self.album = self.get_album()
        return self.album.photo_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        back_link = reverse('photo:albums'), _('Albums')
        location = None
        if 'location_pk' in self.kwargs:
            location = get_object_or_404(Location, pk=self.kwargs.get('location_pk'))
            back_link = reverse('location', kwargs={'pk': location.pk}), location.name

        context['location'] = location
        context['back_link'] = back_link
        context['page_title'] = self.album.name
        context['album'] = self.album
        return context

detail = Detail.as_view()