from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from django.core.exceptions import ValidationError

from backend.common.choices import AccionesProgramaDeAsignatura
from backend.models import Asignatura
from backend.services import (
    ServicioRoles,
    ServicioVersionProgramaAsignatura,
    ServicioAuditoria,
)
from backend.common.mensajes_de_error import (
    MENSAJE_ID_INEXISTENTE,
    MENSAJE_PERMISO_PROGRAMA,
    MENSAJE_ERROR_INESPERADO,
)


class ReutilizarUltimoPrograma(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, id_asignatura):
        """
        Obtiene informacion de un programa, modo solo lectura
        """
        servicio_rol = ServicioRoles()
        servicio_programa = ServicioVersionProgramaAsignatura()
        servicio_auditoria = ServicioAuditoria()

        try:
            asignatura = Asignatura.objects.get(id=id_asignatura)
        except Asignatura.DoesNotExist:
            return Response(
                {"error": {"__all__": [MENSAJE_ID_INEXISTENTE]}},
                status=HTTP_400_BAD_REQUEST,
            )

        if servicio_rol.usuario_tiene_permiso_para_crear_programa(
            usuario=request.user, asignatura=asignatura
        ):
            try:
                data = servicio_programa.reutilizar_ultimo_plan(asignatura)
            except ValidationError as e:
                return Response({"error": e.message_dict}, status=HTTP_400_BAD_REQUEST)

            if data is None:
                return Response({"error": {"__all__": [MENSAJE_ERROR_INESPERADO]}})

            servicio_auditoria.auditar_revision(
                request.user,
                data,
                AccionesProgramaDeAsignatura.REUTILIZAR_ULTIMO_PROGRAMA,
            )
            return Response()

        return Response(
            {"error": {"__all__": [MENSAJE_PERMISO_PROGRAMA]}},
            status=HTTP_401_UNAUTHORIZED,
        )
