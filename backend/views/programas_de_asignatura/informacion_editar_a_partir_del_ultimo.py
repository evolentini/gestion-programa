from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from backend.models import VersionProgramaAsignatura, Asignatura
from backend.services import ServicioRoles, ServicioVersionProgramaAsignatura
from backend.serializers import serializer_programa_asignatura
from backend.common.mensajes_de_error import (
    MENSAJE_ID_INEXISTENTE,
    MENSAJE_PERMISO_PROGRAMA,
)


PROGRAMA_VACIO = {
    "id": -1,
    "carga_horaria": {
        "semanas_dictado": "",
        "teoria_presencial": "",
        "practica_presencial": "",
        "teorico_practico_presencial": "",
        "laboratorio_presencial": "",
        "teoria_distancia": "",
        "practica_distancia": "",
        "teorico_practico_distancia": "",
        "laboratorio_distancia": "",
    },
    "descriptores": {
        "resultados_de_aprendizaje": [],
        "ejes_transversales": [],
        "descriptores": [],
        "actividades_reservadas": [],
    },
    "informacion_adicional": {
        "fundamentacion": "",
        "contenidos": "",
        "bibliografia": "",
        "metodologia_aplicada": "",
        "recursos": "",
        "evaluacion": "",
        "investigacion_docentes": "",
        "investigacion_estudiantes": "",
        "extension_docentes": "",
        "extension_estudiantes": "",
    },
    "correlativas": [],
}


class InformacionEditarProgramaAPartirDelUltimoAPI(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, id_asignatura):
        """
        Obtiene informacion necesaria para el formulario de modificacion de un determinado programa.
        Devuelve las opciones posibles de ejes transversales, actividades reservadas, descriptores, etc.
        """
        servicio_rol = ServicioRoles()
        servicio_programa = ServicioVersionProgramaAsignatura()
        try:
            asignatura = Asignatura.objects.get(id=id_asignatura)
        except VersionProgramaAsignatura.DoesNotExist:
            return Response(
                {"error": MENSAJE_ID_INEXISTENTE},
                status=HTTP_400_BAD_REQUEST,
            )

        if servicio_rol.usuario_tiene_permiso_para_crear_programa(
            request.user, asignatura
        ):
            try:
                ultimo_programa = (
                    servicio_programa.obtener_ultimo_programa_de_asignatura_aprobado(
                        asignatura=asignatura
                    )
                )
                # Obtiene los datos del programa, con informacion extra para su modificacion
                data = serializer_programa_asignatura(ultimo_programa)
                return Response({"data": data})
            except VersionProgramaAsignatura.DoesNotExist:
                # en vez de fallar, va a generar datos para crear desde cero
                data = servicio_programa.obtener_datos_para_nuevo_programa(asignatura)
                programa_vacio = {**PROGRAMA_VACIO}
                programa_vacio["descriptores"] = data
                return Response({"data": programa_vacio})

        return Response(
            {"error": MENSAJE_PERMISO_PROGRAMA},
            status=HTTP_401_UNAUTHORIZED,
        )
