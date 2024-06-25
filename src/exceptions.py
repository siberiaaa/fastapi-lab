class Message_Redirection_Exception(Exception):
    def __init__ (self, message: str, path_route: str, path_message: str):
        self.message = message
        self.path_route = path_route
        self.path_message = path_message

class No_Artesano_Exception(Message_Redirection_Exception):
    def __init__(self, message='Para acceder a esta función debes ser otro tipo de usuario.', path_route='/home', path_message='Volver a home.'):
        super().__init__(message, path_route, path_message)

class No_Cliente_Exception(Message_Redirection_Exception):
    def __init__(self, message='Para acceder a esta función debes ser otro tipo de usuario.', path_route='/home', path_message='Volver a home.'):
        super().__init__(message, path_route, path_message)
