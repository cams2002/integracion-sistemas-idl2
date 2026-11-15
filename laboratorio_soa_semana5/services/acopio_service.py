import uuid

from spyne import ServiceBase, srpc, Unicode

from models.leche_models import LoteLecheInput, ResultadoRecepcionOutput


class HolaMundoService(ServiceBase):

    @srpc(Unicode, _returns=Unicode)
    def saludar_centro_acopio(nombre_centro):
        """Método para validación inicial de conectividad SOAP."""
        return f"Conexión exitosa con ERP Gloria. Bienvenido Centro de Acopio: {nombre_centro}"


class AcopioLecheService(ServiceBase):

    @srpc(LoteLecheInput, _returns=ResultadoRecepcionOutput)
    def registrar_lote_leche(lote):
        """
        Procesa el registro del lote enviado por el cliente Zeep.
        Regla de calidad Gloria: acidez permitida entre 13.0 °D y 18.0 °D.
        """
        id_tx = f"TX-GLORIA-{uuid.uuid4().hex[:8].upper()}"

        # Validación básica de datos
        if lote.litros_ingresados <= 0:
            return ResultadoRecepcionOutput(
                id_transaccion=id_tx,
                estado_registro="RECHAZADO",
                control_calidad_aprobado=False,
                observaciones="El volumen en litros ingresado debe ser mayor a cero."
            )

        # Evaluación de la prueba de acidez Dornic
        acidez = lote.prueba_acidez

        if 13.0 <= acidez <= 18.0:
            return ResultadoRecepcionOutput(
                id_transaccion=id_tx,
                estado_registro="APROBADO",
                control_calidad_aprobado=True,
                observaciones=f"Lote del ganadero {lote.id_ganadero} aceptado. Acidez óptima ({acidez} °D)."
            )
        elif acidez < 13.0:
            return ResultadoRecepcionOutput(
                id_transaccion=id_tx,
                estado_registro="RECHAZADO",
                control_calidad_aprobado=False,
                observaciones=f"Lote del ganadero {lote.id_ganadero} rechazado. Acidez baja ({acidez} °D): posible adulteración con agua o neutralizantes."
            )
        else:
            return ResultadoRecepcionOutput(
                id_transaccion=id_tx,
                estado_registro="RECHAZADO",
                control_calidad_aprobado=False,
                observaciones=f"Lote del ganadero {lote.id_ganadero} rechazado. Acidez alta ({acidez} °D): posible proliferación bacteriana o mala refrigeración."
            )