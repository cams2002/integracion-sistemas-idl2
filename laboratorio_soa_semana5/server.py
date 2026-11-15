import logging
from wsgiref.simple_server import make_server

from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from services.acopio_service import HolaMundoService, AcopioLecheService

# Configuración de logging
logging.basicConfig(level=logging.INFO)

# Definición de la aplicación Spyne con múltiples servicios
application = Application(
    [HolaMundoService, AcopioLecheService],
    tns="gloria.erp.acopio",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 8000

    print("========== Servidor SOAP ERP Gloria iniciando ==========")
    print(f"WSDL disponible en: http://{HOST}:{PORT}/?wsdl")
    print("========================================================")

    server = make_server(HOST, PORT, wsgi_app)
    server.serve_forever()