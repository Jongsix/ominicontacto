# -*- coding: utf-8 -*-
# Copyright (C) 2018 Freetech Solutions

# This file is part of OMniLeads

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

"""
Servicio para generar reporte csv para un agente el cual muestrar todas las
gestiones(ventas) de un agente
"""

from __future__ import unicode_literals

import csv
import logging
import os
import datetime
import json

from ominicontacto_app.utiles import crear_archivo_en_media_root

from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.encoding import force_text


logger = logging.getLogger(__name__)


class ArchivoDeReporteCsv(object):
    def __init__(self, agente):
        self._agente = agente
        self.nombre_del_directorio = 'reporte_agente'
        self.prefijo_nombre_de_archivo = "{0}-reporte_agente".format(
            self._agente.id)
        self.sufijo_nombre_de_archivo = ".csv"
        self.nombre_de_archivo = "{0}{1}".format(
            self.prefijo_nombre_de_archivo, self.sufijo_nombre_de_archivo)
        self.url_descarga = os.path.join(settings.MEDIA_URL,
                                         self.nombre_del_directorio,
                                         self.nombre_de_archivo)
        self.ruta = os.path.join(settings.MEDIA_ROOT,
                                 self.nombre_del_directorio,
                                 self.nombre_de_archivo)

    def crear_archivo_en_directorio(self):
        if self.ya_existe():
            # Esto puede suceder si en un intento previo de depuracion, el
            # proceso es abortado, y por lo tanto, el archivo puede existir.
            logger.warn(_("ArchivoDeReporteCsv: Ya existe archivo CSV de "
                          "reporte para el agente {0}. Archivo: {1}. "
                          "El archivo sera sobreescrito".format(self._agente.pk,
                                                                self.ruta)))

        crear_archivo_en_media_root(
            self.nombre_del_directorio,
            self.prefijo_nombre_de_archivo,
            self.sufijo_nombre_de_archivo)

    def escribir_archivo_csv(self, formularios):

        with open(self.ruta, 'wb') as csvfile:
            # Creamos encabezado
            encabezado = []

            encabezado.append(_("Telefono"))
            encabezado.append(_("datos del cliente"))

            # Creamos csvwriter
            csvwiter = csv.writer(csvfile)

            # guardamos encabezado
            lista_encabezados_utf8 = [force_text(item).encode('utf-8')
                                      for item in encabezado]
            csvwiter.writerow(lista_encabezados_utf8)

            # Iteramos cada una de las calificaciones del agente
            for metadata in formularios:
                lista_opciones = []

                # --- Buscamos datos

                lista_opciones.append(metadata.contacto.telefono)

                datos = json.loads(metadata.contacto.datos)
                for dato in datos:
                    lista_opciones.append(dato)
                datos = json.loads(metadata.metadata)
                for clave, valor in datos.items():
                    lista_opciones.append(valor)

                # --- Finalmente, escribimos la linea

                lista_opciones_utf8 = [force_text(item).encode('utf-8')
                                       for item in lista_opciones]
                csvwiter.writerow(lista_opciones_utf8)

    def ya_existe(self):
        return os.path.exists(self.ruta)


class ReporteFormularioVentaService(object):

    def crea_reporte_csv(self, agente, fecha_desde, fecha_hasta):
        # assert campana.estado == Campana.ESTADO_ACTIVA

        archivo_de_reporte = ArchivoDeReporteCsv(agente)

        archivo_de_reporte.crear_archivo_en_directorio()

        formularios = self._obtener_listado_formularios_fecha(agente,
                                                              fecha_desde,
                                                              fecha_hasta)

        archivo_de_reporte.escribir_archivo_csv(formularios)

    def obtener_url_reporte_csv_descargar(self, agente):
        # assert campana.estado == Campana.ESTADO_DEPURADA

        archivo_de_reporte = ArchivoDeReporteCsv(agente)
        if archivo_de_reporte.ya_existe():
            return archivo_de_reporte.url_descarga

        # Esto no debería suceder.
        logger.error(_("obtener_url_reporte_csv_descargar(): NO existe archivo"
                       " CSV de descarga para el agente {0}".format(agente.pk)))

    def _obtener_listado_formularios_fecha(self, agente, fecha_desde,
                                           fecha_hasta):
        fecha_desde = datetime.datetime.combine(fecha_desde, datetime.time.min)
        fecha_hasta = datetime.datetime.combine(fecha_hasta, datetime.time.max)
        return agente.metadataagente.filter(fecha__range=(fecha_desde, fecha_hasta))
