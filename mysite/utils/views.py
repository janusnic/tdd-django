from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView, RedirectView

__all__ = ['AjaxFormView', 'AjaxCreateView', 'AjaxUpdateView', 'AjaxDeleteView', 'RedirectView']


class AjaxFormMixin:
    """
    Provides methods to return JSON responses for Django's class-based form views.
    """

    def json(self, **data):
        return JsonResponse(data)

    def form_valid(self, form):
        return self.json(url=self.get_success_url())

    def render_to_response(self, context, **kwargs):
        response = super().render_to_response(context, **kwargs)
        return self.json(html=response.rendered_content)


class AjaxCreateView(AjaxFormMixin, CreateView):
    """
    Just like a normal CreateView, except it will return JSON responses.
    """

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class AjaxUpdateView(AjaxFormMixin, UpdateView):
    """
    Just like a normal UpdateView, except it will return JSON responses.
    """

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class AjaxDeleteView(AjaxFormMixin, DeleteView):
    """
    Just like a normal DeleteView, except it will return JSON responses
    if the request was a JSON request.
    """

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return self.json(url=success_url)
