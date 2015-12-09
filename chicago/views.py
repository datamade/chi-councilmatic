from django.shortcuts import render
from datetime import date, timedelta
from chicago.models import ChicagoBill
from councilmatic_core.models import Event
from councilmatic_core.views import *


class ChicagoIndexView(IndexView):
    template_name = 'chicago/index.html'
    bill_model = ChicagoBill

class ChicagoAboutView(AboutView):
    template_name = 'chicago/about.html'

class ChicagoBillDetailView(BillDetailView):
    model = ChicagoBill

    def get_object(self, queryset=None):
        """
        Returns a bill based on slug. If no bill found,
        looks for bills based on legistar id (so that
        urls from old Chicago councilmatic don't break)
        """

        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        # Try looking up by slug
        if slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:

            # Try looking up by legistar id
            pattern = '?ID=%s&GUID' %slug

            try:
                obj = ChicagoBill.objects.get(source_url__contains=pattern)
            except:
                raise Http404("No bill found matching the query")
        return obj
