# -*- coding: utf-8 -*-

"""
Vista para administrar el modelo Campana de tipo dialer
Observacion se copiaron varias vistas del modulo views_campana
"""

from __future__ import unicode_literals

import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from ominicontacto_app.models import Campana, AgenteProfile
from django.views.generic import (
    ListView, UpdateView, FormView, DeleteView
)
from django.views.generic.base import RedirectView
from ominicontacto_app.services.reporte_campana_manual_calificacion import \
    ReporteCampanaService
from ominicontacto_app.services.reporte_campana_manual_gestion import \
    ReporteGestionCampanaService
from ominicontacto_app.services.estadisticas_campana_manuales import EstadisticasService
from ominicontacto_app.forms import ReporteForm
from ominicontacto_app.utiles import convert_fecha_datetime
from ominicontacto_app.services.reporte_manual_agente import EstadisticasAgenteService
from ominicontacto_app.views_campana import CampanaSupervisorUpdateView, CampanasDeleteMixin


import logging as logging_

logger = logging_.getLogger(__name__)


class CampanaManualListView(ListView):
    """
    Esta vista lista los objetos Campana de type dialer
    Vista copiada
    """

    template_name = 'campana_manual/campana_list.html'
    context_object_name = 'campanas'
    model = Campana

    def _get_campanas(self):
        return Campana.objects.obtener_campanas_manuales()

    def get_context_data(self, **kwargs):
        context = super(CampanaManualListView, self).get_context_data(**kwargs)
        campanas = self._get_campanas()
        # Filtra las campanas de acuerdo al usuario logeado si tiene permiso sobre
        # las mismas
        if self.request.user.is_authenticated() and self.request.user and \
                not self.request.user.get_is_administrador():
            user = self.request.user
            campanas = Campana.objects.obtener_campanas_vista_by_user(campanas, user)
            context['campanas'] = campanas

        context['activas'] = campanas.filter(estado=Campana.ESTADO_ACTIVA)
        context['borradas'] = campanas.filter(estado=Campana.ESTADO_BORRADA,
                                              oculto=False)
        context['campanas'] = campanas
        return context


class CampanaManualReporteCalificacionListView(ListView):
    """
    Muestra un listado de contactos a los cuales se los calificaron en la campana
    """
    template_name = 'campana_manual/reporte_campana_formulario.html'
    context_object_name = 'campana'
    model = Campana

    def get_context_data(self, **kwargs):
        context = super(CampanaManualReporteCalificacionListView, self).get_context_data(
            **kwargs)

        service = ReporteCampanaService()
        service_formulario = ReporteGestionCampanaService()
        campana = Campana.objects.get(pk=self.kwargs['pk_campana'])
        service.crea_reporte_csv(campana)
        service_formulario.crea_reporte_csv(campana)
        context['campana'] = campana
        return context


class ExportaReporteFormularioGestionView(UpdateView):
    """
    Esta vista invoca a generar un csv de reporte de la la venta.
    """

    model = Campana
    context_object_name = 'campana'

    def get_object(self, queryset=None):
        return Campana.objects.get(pk=self.kwargs['pk_campana'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        service = ReporteGestionCampanaService()
        url = service.obtener_url_reporte_csv_descargar(self.object)
        return redirect(url)


class ExportaReporteCampanaManualView(UpdateView):
    """
    Esta vista invoca a generar un csv de reporte de la campana.
    """

    model = Campana
    context_object_name = 'campana'

    def get_object(self, queryset=None):
        return Campana.objects.get(pk=self.kwargs['pk_campana'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        service = ReporteCampanaService()
        url = service.obtener_url_reporte_csv_descargar(self.object)
        return redirect(url)


class CampanaManualReporteGrafico(FormView):
    """Esta vista genera el reporte grafico de la campana"""

    template_name = 'campana_manual/reporte_grafico.html'
    context_object_name = 'campana'
    model = Campana
    form_class = ReporteForm

    def get_object(self, queryset=None):
        return Campana.objects.get(pk=self.kwargs['pk_campana'])

    def get(self, request, *args, **kwargs):
        service = EstadisticasService()
        hoy_ahora = datetime.datetime.today()
        hoy = hoy_ahora.date()
        # genera los reportes grafico de la campana
        graficos_estadisticas = service.general_campana(self.get_object(), hoy,
                                                        hoy_ahora)

        return self.render_to_response(self.get_context_data(
            graficos_estadisticas=graficos_estadisticas,
            pk_campana=self.kwargs['pk_campana']))

    def get_context_data(self, **kwargs):
        context = super(CampanaManualReporteGrafico, self).get_context_data(
            **kwargs)

        context['campana'] = self.get_object()
        return context

    def form_valid(self, form):
        fecha = form.cleaned_data.get('fecha')
        fecha_desde, fecha_hasta = fecha.split('-')
        fecha_desde = convert_fecha_datetime(fecha_desde)
        fecha_hasta = convert_fecha_datetime(fecha_hasta)
        # generar el reporte grafico de acuerdo al periodo de fecha seleccionado
        service = EstadisticasService()
        graficos_estadisticas = service.general_campana(
            self.get_object(), fecha_desde, fecha_hasta)
        return self.render_to_response(self.get_context_data(
            graficos_estadisticas=graficos_estadisticas,
            pk_campana=self.kwargs['pk_campana']))


class AgenteCampanaManualReporteGrafico(FormView):
    """Esta vista genera el reporte grafico de la campana para un agente
    copiada del modulo views_campana"""
    template_name = 'campana/reporte_agente.html'
    context_object_name = 'campana'
    model = Campana
    form_class = ReporteForm

    def get_object(self, queryset=None):
        return Campana.objects.get(pk=self.kwargs['pk_campana'])

    def get(self, request, *args, **kwargs):
        service = EstadisticasAgenteService()
        hoy_ahora = datetime.datetime.today()
        hoy = hoy_ahora.date()
        agente = AgenteProfile.objects.get(pk=self.kwargs['pk_agente'])
        # generar el reporte para el agente de esta campana
        graficos_estadisticas = service.general_campana(agente,
                                                        self.get_object(), hoy,
                                                        hoy_ahora)
        return self.render_to_response(self.get_context_data(
            graficos_estadisticas=graficos_estadisticas))

    def get_context_data(self, **kwargs):
        context = super(AgenteCampanaManualReporteGrafico, self).get_context_data(
            **kwargs)

        agente = AgenteProfile.objects.get(pk=self.kwargs['pk_agente'])
        context['pk_campana'] = self.kwargs['pk_campana']

        context['agente'] = agente
        return context

    def form_valid(self, form):
        fecha = form.cleaned_data.get('fecha')
        fecha_desde, fecha_hasta = fecha.split('-')
        fecha_desde = convert_fecha_datetime(fecha_desde)
        fecha_hasta = convert_fecha_datetime(fecha_hasta)
        # genera el reporte para el agente de esta campana
        service = EstadisticasAgenteService()
        agente = AgenteProfile.objects.get(pk=self.kwargs['pk_agente'])
        graficos_estadisticas = service.general_campana(agente,
                                                        self.get_object(),
                                                        fecha_desde,
                                                        fecha_hasta)
        return self.render_to_response(self.get_context_data(
            graficos_estadisticas=graficos_estadisticas))


class CampanaManualDeleteView(CampanasDeleteMixin, DeleteView):
    """
    Esta vista se encarga de la eliminación de una campana
    """
    model = Campana
    template_name = 'campana_manual/delete_campana.html'

    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        super(CampanaManualDeleteView, self).delete(request, *args, **kwargs)
        return HttpResponseRedirect(success_url)

    def get_object(self, queryset=None):
        return Campana.objects.get(pk=self.kwargs['pk_campana'])

    def get_success_url(self):
        return reverse('campana_manual_list')


class OcultarCampanaManualView(RedirectView):
    """
    Esta vista actualiza la campañana ocultandola.
    """

    pattern_name = 'campana_manual_list'

    def get(self, request, *args, **kwargs):
        campana = Campana.objects.get(pk=self.kwargs['pk_campana'])
        campana.ocultar()
        return HttpResponseRedirect(reverse('campana_manual_list'))


class DesOcultarCampanaManualView(RedirectView):
    """
    Esta vista actualiza la campañana haciendola visible.
    """

    pattern_name = 'campana_manual_list'

    def get(self, request, *args, **kwargs):
        campana = Campana.objects.get(pk=self.kwargs['pk_campana'])
        campana.desocultar()
        return HttpResponseRedirect(reverse('campana_manual_list'))


class CampanaManualSupervisorUpdateView(CampanaSupervisorUpdateView):
    """
    Esta vista agrega supervisores a una campana manual
    logica copiado para campana_preview
    """

    def get_success_url(self):
        return reverse('campana_manual_list')


class CampanaManualBorradasListView(CampanaManualListView):
    """
    Vista que lista las campañas manual pero de incluyendo las borradas ocultas
    """

    template_name = 'campana_manual/campanas_borradas.html'

    def get_context_data(self, **kwargs):
        context = super(CampanaManualBorradasListView, self).get_context_data(**kwargs)
        context['borradas'] = context['campanas'].filter(estado=Campana.ESTADO_BORRADA)
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super(CampanaManualBorradasListView, self).get(request, *args, **kwargs)
        else:
            return JsonResponse({'result': 'desconectado'})
