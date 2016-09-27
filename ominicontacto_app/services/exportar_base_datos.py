# -*- coding: utf-8 -*-

"""
Servicio de exportacion de base de datos de contactos para discador
"""

from __future__ import unicode_literals

import csv
import logging
import os
import json


from django.conf import settings
from ominicontacto_app.utiles import crear_archivo_en_media_root
from django.utils.encoding import force_text
from ominicontacto_app.models import Contacto, Campana

logger = logging.getLogger(__name__)


class ArchivoDeReporteCsv(object):
    def __init__(self, base_datos):
        self._base_datos = base_datos
        self.nombre_del_directorio = 'base_datos_contacto'
        self.prefijo_nombre_de_archivo = "{0}-exportar".format(
            self._base_datos.id)
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
                        "El archivo sera sobreescrito", self._base_datos.pk,
                        self.ruta)

        crear_archivo_en_media_root(
            self.nombre_del_directorio,
            self.prefijo_nombre_de_archivo,
            self.sufijo_nombre_de_archivo)

    def escribir_archivo_csv(self, contactos, metadata, campana, telefonos,
                             usa_contestador):

        with open(self.ruta, 'wb') as csvfile:
            nombres_de_columnas = metadata.nombres_de_columnas

            # Creamos encabezado
            encabezado = []
            encabezado.append("telefono")
            encabezado.append("id_cliente")
            encabezado.append("nombre")
            encabezado.append("campana")
            encabezado.append("timeout")
            encabezado.append("id_campana")
            encabezado.append("usa_contestador")
            for columna in telefonos:
                encabezado.append(nombres_de_columnas[int(columna)])

            # Creamos csvwriter
            csvwiter = csv.writer(csvfile)

            # guardamos encabezado
            lista_encabezados_utf8 = [force_text(item).encode('utf-8')
                                      for item in encabezado]
            csvwiter.writerow(lista_encabezados_utf8)

            # Iteramos cada uno de los contactos, con los eventos de TODOS los intentos
            for contacto in contactos:
                lista_opciones = []

                # --- Buscamos datos
                lista_opciones.append(contacto.telefono)
                lista_opciones.append(contacto.id_cliente)
                lista_opciones.append(contacto.nombre + "" + contacto.apellido)
                lista_opciones.append(campana.nombre)
                lista_opciones.append(campana.queue_campana.timeout)
                lista_opciones.append(campana.id)
                lista_opciones.append(usa_contestador)
                datos = json.loads(contacto.datos)
                for col_telefono in telefonos:
                    indice_columna_dato = int(col_telefono) - 7
                    lista_opciones.append(datos[indice_columna_dato])

                # --- Finalmente, escribimos la linea

                lista_opciones_utf8 = [force_text(item).encode('utf-8')
                                       for item in lista_opciones]
                csvwiter.writerow(lista_opciones_utf8)

    def ya_existe(self):
        return os.path.exists(self.ruta)


class ExportarBaseDatosContactosService(object):

    def crea_reporte_csv(self, base_datos, campana, telefonos, usa_contestador):
        archivo_de_reporte = ArchivoDeReporteCsv(base_datos)
        archivo_de_reporte.crear_archivo_en_directorio()
        contactos = Contacto.objects.contactos_by_bd_contacto(base_datos)
        metadata = base_datos.get_metadata()
        campana = Campana.objects.get(pk=campana)
        archivo_de_reporte.escribir_archivo_csv(contactos, metadata,campana,
                                                telefonos, usa_contestador)

    def obtener_url_reporte_csv_descargar(self, base_datos):
        archivo_de_reporte = ArchivoDeReporteCsv(base_datos)
        if archivo_de_reporte.ya_existe():
            return archivo_de_reporte.url_descarga

        # Esto no debería suceder.
        logger.error("obtener_url_reporte_csv_descargar(): NO existe archivo"
                     " CSV de descarga para la base de datos %s", base_datos.pk)
        assert os.path.exists(archivo_de_reporte.url_descarga)