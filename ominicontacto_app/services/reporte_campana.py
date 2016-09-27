# -*- coding: utf-8 -*-

"""
Servicio de reportes de campanas
"""

from __future__ import unicode_literals

import csv
import logging
import os


from django.conf import settings
from ominicontacto_app.utiles import crear_archivo_en_media_root
from django.utils.encoding import force_text


logger = logging.getLogger(__name__)


class ArchivoDeReporteCsv(object):
    def __init__(self, campana):
        self._campana = campana
        self.nombre_del_directorio = 'reporte_campana'
        self.prefijo_nombre_de_archivo = "{0}-reporte".format(self._campana.id)
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
            logger.warn("ArchivoDeReporteCsv: Ya existe archivo CSV de "
                        "reporte para la campana %s. Archivo: %s. "
                        "El archivo sera sobreescrito", self._campana.pk,
                        self.ruta)

        crear_archivo_en_media_root(
            self.nombre_del_directorio,
            self.prefijo_nombre_de_archivo,
            self.sufijo_nombre_de_archivo)

    def escribir_archivo_csv(self, campana):

        with open(self.ruta, 'wb') as csvfile:
            # Creamos encabezado
            encabezado = []


            encabezado.append("Id Cliente")
            encabezado.append("Nombre")
            encabezado.append("Apellido")
            encabezado.append("Telefono")
            encabezado.append("email")
            encabezado.append("datos")

            for c in range(10):
                encabezado.append("Extra_{0}".format(c + 1))

            # Creamos csvwriter
            csvwiter = csv.writer(csvfile)

            # guardamos encabezado
            lista_encabezados_utf8 = [force_text(item).encode('utf-8')
                                      for item in encabezado]
            csvwiter.writerow(lista_encabezados_utf8)

            # Iteramos cada uno de los contactos, con los eventos de TODOS los intentos
            for formulario in campana.formularios.all():
                lista_opciones = []

                # --- Buscamos datos


                lista_opciones.append(formulario.contacto.id_cliente)
                lista_opciones.append(formulario.contacto.nombre)
                lista_opciones.append(formulario.contacto.apellido)
                lista_opciones.append(formulario.contacto.telefono)
                lista_opciones.append(formulario.contacto.email)
                lista_opciones.append(formulario.contacto.datos)
                lista_opciones.append(formulario.extra_1)
                lista_opciones.append(formulario.extra_2)
                lista_opciones.append(formulario.extra_3)
                lista_opciones.append(formulario.extra_4)
                lista_opciones.append(formulario.extra_5)
                lista_opciones.append(formulario.extra_6)
                lista_opciones.append(formulario.extra_7)
                lista_opciones.append(formulario.extra_8)
                lista_opciones.append(formulario.extra_9)
                lista_opciones.append(formulario.extra_10)

                # --- Finalmente, escribimos la linea

                lista_opciones_utf8 = [force_text(item).encode('utf-8')
                                       for item in lista_opciones]
                csvwiter.writerow(lista_opciones_utf8)

    def ya_existe(self):
        return os.path.exists(self.ruta)


class ReporteCampanaService(object):

    def crea_reporte_csv(self, campana):
        #assert campana.estado == Campana.ESTADO_ACTIVA

        archivo_de_reporte = ArchivoDeReporteCsv(campana)

        archivo_de_reporte.crear_archivo_en_directorio()

        #opciones_por_contacto = self._obtener_opciones_por_contacto(campana)

        archivo_de_reporte.escribir_archivo_csv(campana)

    def obtener_url_reporte_csv_descargar(self, campana):
        #assert campana.estado == Campana.ESTADO_DEPURADA

        archivo_de_reporte = ArchivoDeReporteCsv(campana)
        if archivo_de_reporte.ya_existe():
            return archivo_de_reporte.url_descarga

        # Esto no debería suceder.
        logger.error("obtener_url_reporte_csv_descargar(): NO existe archivo"
                     " CSV de descarga para la campana %s", campana.pk)
        assert os.path.exists(archivo_de_reporte.url_descarga)