from django.views.generic import TemplateView, ListView, DetailView
from .models import Item, Photo

class IndexPageView(TemplateView):

    template_name = "gallery/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context['item_list'] = Item.objects.all()[:3]
        return context

class ItemsListView(ListView):

    template_name = "gallery/items_listing.html"

    model = Item

class ItemObjectView(DetailView):

    template_name = "gallery/items_detail.html"

    model = Item

class PhotoObjectView(DetailView):

    template_name = "gallery/photo_detail.html"

    model = Photo