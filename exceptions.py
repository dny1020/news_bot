from flask import jsonify

# Excepción personalizada para errores de API
class APIError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code or 500

    def to_dict(self):
        return {"error": self.message}

# Manejador general de excepciones
def handle_generic_exception(e):
    response = jsonify({"error": "Ha ocurrido un error en el servidor."})
    response.status_code = 500
    return response

# Manejador de errores 404 (Página no encontrada)
def handle_404_error(e):
    response = jsonify({"error": "Recurso no encontrado."})
    response.status_code = 404
    return response

# Manejador de errores de API
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
