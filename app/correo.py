from notificacion import Notificacion

class Correo(Notificacion):
    def enviar_notificacion(self, mensaje: str):
        if self.persona.correo:
            print(f'Enviando correo a {self.persona.correo}: {mensaje}')
        else:
            print('Correo no disponible para esta persona.')
