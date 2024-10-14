from notificacion import Notificacion
import csv
from datetime import datetime

class Cita:
    def __init__(self, paciente, medico, fecha_hora):
        self.paciente = paciente
        self.medico = medico
        self.fecha_hora = fecha_hora
        self.motivo_cancelacion = None

    @staticmethod
    def cargar_citas(archivo, pacientes, medicos):
        citas = []
        with open(archivo, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                paciente = next((p for p in pacientes if p.identificacion == row['paciente']), None)
                medico = next((m for m in medicos if m.id == row['medico']), None)
                if paciente and medico:
                    fecha_hora = datetime.strptime(row['fecha_hora'], "%Y-%m-%d %H:%M")
                    if medico.verificar_disponibilidad(fecha_hora):
                        cita = Cita(paciente=paciente, medico=medico, fecha_hora=fecha_hora)
                        medico.agenda.agendar_cita(cita)  # Añadir cita a la agenda del médico
                        citas.append(cita)
        return citas

    def recordatorio_cita(self):
        mensaje = f"Recuerde su cita con el Dr. {self.medico.nombre} el {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}."
        self.paciente.enviar_notificacion("Recordatorio de Cita", mensaje)

    def reprogramar_cita(self, nueva_fecha_hora):
        nueva_fecha_hora_dt = datetime.strptime(nueva_fecha_hora, "%Y-%m-%d %H:%M")
        if self.medico.verificar_disponibilidad(nueva_fecha_hora_dt):
            old_fecha_hora = self.fecha_hora
            self.fecha_hora = nueva_fecha_hora_dt
            self.medico.agenda.reprogramar_cita(self, old_fecha_hora)  # Reprogramar en la agenda del médico
            print(f"Cita reprogramada del {old_fecha_hora} al {self.fecha_hora}")
            # Notificar al paciente sobre la reprogramación
            mensaje = (f"Su cita con el Dr. {self.medico.nombre} ha sido reprogramada del "
                       f"{old_fecha_hora.strftime('%Y-%m-%d %H:%M')} al {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}.")
            self.paciente.enviar_notificacion("Reprogramación de Cita", mensaje)
        else:
            print(f"No hay disponibilidad para reprogramar la cita en la fecha {nueva_fecha_hora}")

    def cancelar_cita(self, motivo):
        self.motivo_cancelacion = motivo
        print(f"La cita ha sido cancelada por {self.paciente.nombre}, debido a: {self.motivo_cancelacion}")
        # Notificar al paciente y al médico sobre la cancelación
        mensaje = (f"Su cita con el Dr. {self.medico.nombre} el {self.fecha_hora.strftime('%Y-%m-%d %H:%M')} "
                   f"ha sido cancelada debido a: {self.motivo_cancelacion}.")
        self.paciente.enviar_notificacion("Cancelación de Cita", mensaje)
        self.medico.enviar_notificacion_agenda(mensaje)
        self.medico.agenda.eliminar_cita(self)  # Eliminar la cita de la agenda del médico

    def __repr__(self):
        return f"Cita del paciente {self.paciente.nombre} con el Dr. {self.medico.nombre} programada para el {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"
