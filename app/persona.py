class Persona:
    def __init__(self, identificacion: str, nombre: str, correo: str, celular: str, whatsapp: str = None):
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.celular = celular
        self.whatsapp = whatsapp

    def __str__(self):
        return f'{self.nombre} (Correo: {self.correo}, Celular: {self.celular}, WhatsApp: {self.whatsapp})'
