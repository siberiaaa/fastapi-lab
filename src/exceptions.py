class Message_Redirection_Exception(Exception):
    def __init__ (self, message: str, path_route: str, path_message: str):
        self.message = message
        self.path_route = path_route
        self.path_message = path_message