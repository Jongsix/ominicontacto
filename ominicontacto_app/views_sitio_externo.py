# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.edit import (
    CreateView
)
from django.views.generic import (
    ListView
)
from django.views.generic.base import RedirectView
from ominicontacto_app.models import SitioExterno
from ominicontacto_app.forms import SitioExternoForm


class SitioExternoCreateView(CreateView):
    model = SitioExterno
    template_name = 'sitio_externo/create_update_form.html'
    form_class = SitioExternoForm

    def get_success_url(self):
        return reverse('sitio_externo_list')


class SitioExternoListView(ListView):
    """
    Esta vista es para generar el listado de
    Lista de Contactos.
    """

    template_name = 'sitio_externo/sitio_externo_list.html'
    context_object_name = 'sitios_externos'
    model = SitioExterno

    def get_queryset(self):
        queryset = SitioExterno.objects.filter(oculto=False)
        return queryset


class OcultarSitioExternoView(RedirectView):
    """
    Esta vista actualiza el sitio externo ocultandola.
    """

    pattern_name = 'sitio_externo_list'

    def get(self, request, *args, **kwargs):
        sitio = SitioExterno.objects.get(pk=self.kwargs['pk_sitio_externo'])
        sitio.ocultar()
        return HttpResponseRedirect(reverse('sitio_externo_list'))


class DesOcultarSitioExternoView(RedirectView):
    """
    Esta vista actualiza el sitio externo haciendolo visible.
    """

    pattern_name = 'sitio_externo_list'

    def get(self, request, *args, **kwargs):
        sitio = SitioExterno.objects.get(pk=self.kwargs['pk_sitio_externo'])
        sitio.desocultar()
        return HttpResponseRedirect(reverse('sitio_externo_list'))


def mostrar_sitio_externos_ocultos_view(request):
    sitios = SitioExterno.objects.all()
    data = {
        'sitios_externos': sitios,
    }
    return render(request, 'sitio_externo/sitios_ocultos.html', data)
