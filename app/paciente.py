from persona import Persona
from agenda import Agenda
from cita import Cita
from notificacion import Notificacion
from correo import Correo
from sms import SMS
from whatsapp import WhatsApp
import csv

class Paciente(Persona):
    def __init__(self, identificacion, nombre, celular, correo,whatsapp = None):
        super().__init__(identificacion, nombre, celular,whatsapp)
        self.medico_preferencia = None
        self.agenda = Agenda()  # Agenda del paciente
        
    @staticmethod
    def cargar_pacientes(archivo):
        pacientes = []
        with open(archivo, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                paciente = Paciente(
                    identificacion=row['identificación'],
                    nombre_completo=row['nombre_completo'],
                    celular=row['celular'],
                    correo=row['correo']
                )
                pacientes.append(paciente)
        return pacientes
    
    def asignar_medico_preferencia(self, medico):
        self.medico_preferencia = medico
        print(f"El médico {medico.nombre} ha sido asignado como preferencia para el paciente {self.nombre}")

    def enviar_confirmacion(self, asunto, mensaje):
        # Puedes personalizar qué métodos de notificación utilizar !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        notificaciones = [
            Correo(persona=self),
            SMS(persona=self),
            WhatsApp(persona=self)
        ]
        for notificacion in notificaciones:
            notificacion.enviar_notificacion(f'{asunto}: {mensaje}')