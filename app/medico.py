from persona import Persona
from agenda import Agenda
from correo import Correo
from celular import Celular
from whatsapp import WhatsApp
import json

class Medico(Persona):
    def __init__(self, identificacion, nombre, correo, celular, especialidad, whatsapp=None):
        super().__init__(identificacion, nombre, correo, celular, whatsapp)
        self.especialidad = especialidad
        self.agenda = Agenda()
        
    @staticmethod
    def cargar_medicos(archivo):
        medicos = []
        with open(archivo, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            for item in data:
                medico = Medico(
                    id=item['id'],
                    nombre=item['nombre'],
                    correo=item['correo'],
                    especialidad=item['especialidad']
                )
                medicos.append(medico)
        return medicos

    def verificar_disponibilidad(self, fecha_hora):
        return fecha_hora not in self.agenda.citas_pendientes

    def enviar_notificacion_agenda(self, mensaje):
        notificaciones = [
            Correo(persona=self),
            Celular(persona=self),
            WhatsApp(persona=self)
        ]
        for notificacion in notificaciones:
            notificacion.enviar_notificacion(f'Notificación de Agenda: {mensaje}')

    def __repr__(self):
        return f"Dr. {self.nombre}, Especialidad: {self.especialidad}"
