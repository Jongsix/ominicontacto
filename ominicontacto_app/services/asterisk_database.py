# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ominicontacto_app.utiles import elimina_espacios
from ominicontacto_app.models import Campana, AgenteProfile, Pausa
from ominicontacto_app.services.asterisk_ami_http import AsteriskHttpClient,\
    AsteriskHttpAsteriskDBError
from configuracion_telefonia_app.models import RutaSaliente, TroncalSIP
import logging as _logging

logger = _logging.getLogger(__name__)


class AbstractFamily(object):
    """class abstract de family de asterisk"""

    def _genera_dict(self):
        raise (NotImplementedError())

    def create_dict(self, family_member):
        raise (NotImplementedError())

    def create_family(self, family_member):
        """Crea family en database de asterisk
        """

        client = AsteriskHttpClient()
        client.login()
        family = self._get_nombre_family(family_member)
        logger.info("Creando familys para la family  %s", family)
        variables = self.create_dict(family_member)
        for key, val in variables.items():
            try:
                client.asterisk_db("DBPut", family, key, val=val)
            except AsteriskHttpAsteriskDBError:
                logger.exception("Error al intentar DBPut al insertar"
                                 " en la family {0} la siguiente key={1}"
                                 " y val={2}".format(family, key, val))

    def _obtener_todos(self):
        raise (NotImplementedError())

    def create_families(self, modelo=None, modelos=None):
        """Crea familys en database de asterisk
        """

        if modelos:
            pass
        elif modelo:
            modelos = [modelo]
        else:
            modelos = self._obtener_todos()

        for familia_member in modelos:
            self.create_family(familia_member)

    def _get_nombre_family(self, family_member):
        raise (NotImplementedError())

    def delete_tree_family(self, family):
        """Elimina el tree de la family pasada por parametro"""
        try:
            client = AsteriskHttpClient()
            client.login()
            client.asterisk_db_deltree(family)
        except AsteriskHttpAsteriskDBError:
            logger.exception("Error al intentar DBDelTree de {0}".format(family))

    def _existe_family_key(self, family, key):
        """Consulta en la base de datos si existe la family y clave"""

        try:
            client = AsteriskHttpClient()
            client.login()
            db_get = client.asterisk_db("DBGet", family, key=key)
        except AsteriskHttpAsteriskDBError:
            logger.exception("Error al intentar DBGet al consultar con la family {0} y "
                             "la siguiente key={1}".format(family, key))
            return False
        if db_get.response_value == 'success':
            return True

    def _get_family_instance(self):
        if isinstance(self, CampanaFamily):
            return "OML/CAMP"
        elif isinstance(self, AgenteFamily):
            return "OML/AGENT"
        elif isinstance(self, PausaFamily):
            return "OML/PAUSE"
        elif isinstance(self, RutaSalienteFamily):
            return "OML/OUTR"
        elif isinstance(self, TrunkFamily):
            return "OML/TRUNK"
        elif isinstance(self, GlobalsFamily):
            return "OML/GLOBALS"
        else:
            raise (NotImplementedError())

    def regenerar_families(self):
        """regenera la family"""
        self.delete_tree_family(self._get_family_instance())
        self.create_families()


class CampanaFamily(AbstractFamily):

    def _genera_dict(self, campana):

        dict_campana = {
            'QNAME': "{0}_{1}".format(campana.id, elimina_espacios(campana.nombre)),
            'TYPE': campana.type,
            'REC': campana.queue_campana.auto_grabacion,
            'AMD': campana.queue_campana.detectar_contestadores,
            'CALLAGENTACTION': campana.tipo_interaccion,
            'RINGTIME': campana.queue_campana.timeout,
            'QUEUETIME': campana.queue_campana.wait,
            'MAXQCALLS': campana.queue_campana.maxlen,
            'SL': campana.queue_campana.servicelevel,
            'TC': "",  # a partir de esta variable no se usan
            'IDJSON': "",
            'PERMITOCCULT': "",
            'MAXCALLS': "",
            'FAILOVER': "",
        }

        if campana.queue_campana.audio_para_contestadores:
            dict_campana.update({'AMDPLAY': "oml/{0}".format(
                campana.queue_campana.audio_para_contestadores.get_filename_audio_asterisk())})

        if campana.queue_campana.audio_de_ingreso:
            dict_campana.update({'WELCOMEPLAY': "oml/{0}".format(
                campana.queue_campana.audio_de_ingreso.get_filename_audio_asterisk())})

        if campana.formulario:
            dict_campana.update({'IDFORM': campana.formulario.pk})
        else:
            dict_campana.update({'IDFORM': ""})

        if campana.sitio_externo:
            dict_campana.update({'IDEXTERNALURL': campana.sitio_externo.pk})
        else:
            dict_campana.update({'IDEXTERNALURL': ""})

        return dict_campana

    def create_dict(self, campana):
        dict_campana = self._genera_dict(campana)
        return dict_campana

    def _obtener_todos(self):
        """Devuelve las campanas para generar .
        """
        return Campana.objects.obtener_all_dialplan_asterisk()

    def _get_nombre_family(self, campana):
        return "OML/CAMP/{0}".format(campana.id)


class AgenteFamily(AbstractFamily):

    def _genera_dict(self, agente):

        dict_agente = {
            'NAME': agente.user.get_full_name(),
            'SIP': agente.sip_extension,
            'STATUS': ""
        }
        return dict_agente

    def create_dict(self, agente):
        dict_agente = self._genera_dict(agente)
        return dict_agente

    def _obtener_todos(self):
        """Obtengo todos los agentes activos"""
        return AgenteProfile.objects.obtener_activos()

    def _get_nombre_family(self, agente):
        return "OML/AGENT/{0}".format(agente.id)


class PausaFamily(AbstractFamily):

    def _genera_dict(self, pausa):

        dict_pausa = {
            'NAME': pausa.nombre,
        }
        return dict_pausa

    def create_dict(self, pausa):
        dict_pausa = self._genera_dict(pausa)
        return dict_pausa

    def _obtener_todos(self):
        """Obtener todas pausas"""
        return Pausa.objects.activas()

    def _get_nombre_family(self, pausa):
        return "OML/PAUSE/{0}".format(pausa.id)


class RutaSalienteFamily(AbstractFamily):

    def _genera_dict(self, ruta):

        dict_ruta = {
            'NAME': ruta.nombre,
            'RINGTIME': ruta.ring_time,
            'OPTIONS': ruta.dial_options,
            'TRUNKS': len(ruta.secuencia_troncales.all())
        }

        patrones = self._obtener_patrones_ordenados(ruta)
        for orden, patron in patrones:
            if patron.prefix:
                prefix = len(str(patron.prefix))
            else:
                prefix = None
            clave_prefix = "PREFIX/{0}".format(orden)
            clave_prepend = "PREPEND/{0}".format(orden)
            dict_ruta.update({clave_prefix: prefix, clave_prepend: patron.prepend})

        troncales = self._obtener_troncales_ordenados(ruta)
        for orden, troncal in troncales:
            dict_ruta.update({"TRUNK/{0}".format(orden): troncal.troncal.nombre})

        return dict_ruta

    def create_dict(self, ruta):
        dict_ruta = self._genera_dict(ruta)
        return dict_ruta

    def _obtener_todos(self):
        """Obtengo todos las rutas salientes para generar family"""
        return RutaSaliente.objects.all()

    def _obtener_patrones_ordenados(self, ruta):
        """ devuelve patrones ordenados con enumerate"""
        return list(enumerate(ruta.patrones_de_discado.all(), start=1))

    def _obtener_troncales_ordenados(self, ruta):
        """ devuelve troncales ordenados con enumerate"""
        return list(enumerate(ruta.secuencia_troncales.all().order_by("orden"), start=1))

    def _get_nombre_family(self, ruta):
        return "OML/OUTR/{0}".format(ruta.id)

    def delete_family_ruta(self, ruta):
        """Elimina una la family de una ruta"""
        # primero chequeo si existe la family
        family = "OML/OUTR/{0}".format(ruta.id)
        key = "NAME"
        existe_family = self._existe_family_key(family, key)
        if existe_family:
            self.delete_tree_family(family)

    def regenerar_familys_rutas(self, ruta):
        """regenera la family de las rutas"""
        family = self._get_nombre_family(ruta)
        self.delete_tree_family(family)
        self.create_families(modelo=ruta)

    def _regenero_trunks_ruta(self, ruta):
        """
        Regenero las entradas para los trunks en la ruta
            /OML/OUTR/XX/TRUNK/N donde xx es la id de la ruta y N el numero de troncal
        """

        # regenero lo datos de los troncales
        troncales = self._obtener_troncales_ordenados(ruta)
        for orden, troncal in troncales:
            logger.info("Creando familys para troncales %s", troncal.troncal.id)

            try:
                client = AsteriskHttpClient()
                client.login()
                family = "OML/OUTR/{0}".format(ruta.id)
                key = "TRUNK/{0}".format(orden)
                val = troncal.troncal.nombre
                client.asterisk_db("DBPut", family, key=key, val=val)
            except AsteriskHttpAsteriskDBError:
                logger.exception("Error al intentar DBPut al insertar"
                                 " en la family {0} la siguiente key={1}"
                                 " y val={2}".format(family, key, val))

    def regenerar_family_trunk_ruta(self, ruta):
        """regeneros lso troncales de la ruta"""
        family = "OML/OUTR/{0}".format(ruta.id)
        key = "NAME"
        existe_family = self._existe_family_key(family, key)
        if existe_family:
            self._regenero_trunks_ruta(ruta)


class TrunkFamily(AbstractFamily):

    def _genera_dict(self, trunk):

        dict_trunk = {
            'NAME': trunk.nombre,
            'CHANNELS': trunk.canales_maximos,
            'CALLERID': trunk.caller_id,
        }

        return dict_trunk

    def create_dict(self, trunk):
        dict_trunk = self._genera_dict(trunk)
        return dict_trunk

    def _obtener_todos(self):
        """Obtengo todos los troncales sip para generar family"""
        return TroncalSIP.objects.all()

    def _get_nombre_family(self, trunk):
        return "OML/TRUNK/{0}".format(trunk.id)

    def delete_family_trunk(self, trunk):
        """Elimina una la family de una ruta"""
        # primero chequeo si existe la family
        family = self._get_nombre_family(trunk)
        key = "NAME"
        existe_family = self._existe_family_key(family, key)
        if existe_family:
            self.delete_tree_family(family)


class RegenerarAsteriskFamilysOML(object):

    def __init__(self):
        self.campana_family = CampanaFamily()
        self.agente_family = AgenteFamily()
        self.pausa_family = PausaFamily()
        self.globals_family = GlobalsFamily()

    def regenerar_asterisk(self):
        self.campana_family.regenerar_families()
        self.agente_family.regenerar_families()
        self.pausa_family.regenerar_families()
        self.globals_family.regenerar_families()


class GlobalsFamily(AbstractFamily):

    def _genera_dict(self):

        dict_globals = {
            'DEFAULTQUEUETIME': 90,
            'DEFAULTRINGTIME': 45,
            'LANG': 'es',
            'OBJ/1': 'sub-oml-in-check-set,s,1',
            'OBJ/2': 'sub-oml-module-tc,s,1',
            'OBJ/3': 'sub-oml-module-ivr,s,1',
            'OBJ/4': 'sub-oml-module-ext,s,1',
            'OBJ/5': 'sub-oml-hangup,s,1',
            'OBJ/6': 'sub-oml-module-survey,s,1',
            'RECFILEPATH': '/var/spool/asterisk/monitor',
            'TYPECALL/1': 'manualCall',
            'TYPECALL/2': 'dialerCall',
            'TYPECALL/3': 'inboundCall',
            'TYPECALL/4': 'previewCall',
            'TYPECALL/5': 'icsCall',
            'TYPECALL/7': 'internalCall',
            'TYPECALL/8': 'transferCall',
            'TYPECALL/9': 'transferOutNumCall',
        }

        return dict_globals

    def create_dict(self, family_member):
        dict_globals = self._genera_dict()
        return dict_globals

    def _get_nombre_family(self, globales):
        return "OML/GLOBALS"

    def create_families(self):
        """Crea familys en database de asterisk
        """
        self.create_family("")
