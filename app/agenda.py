from datetime import datetime, timedelta

class Agenda:
    def __init__(self):
        self.citas_pendientes = []  # Lista de citas pendientes

    def verificar_disponibilidad(self, fecha_hora):
        """
        Verifica si el médico tiene disponibilidad en la fecha y hora proporcionada.
        """
        for cita in self.citas_pendientes:
            if cita.fecha_hora == fecha_hora:
                return False  # No está disponible en esa fecha y hora
        return True  # Disponible

    def agregar_cita(self, cita):
        """
        Agrega una cita a la lista de citas pendientes si el horario está disponible.
        """
        if self.verificar_disponibilidad(cita.fecha_hora):
            self.citas_pendientes.append(cita)
            print(f"Cita agregada para {cita.paciente.nombre} el {cita.fecha_hora}")
        else:
            print(f"El horario {cita.fecha_hora} no está disponible.")

    def cancelar_cita(self, cita):
        """
        Cancela una cita existente y la elimina de la lista.
        """
        if cita in self.citas_pendientes:
            self.citas_pendientes.remove(cita)
            print(f"Cita cancelada para {cita.paciente.nombre} el {cita.fecha_hora}")
        else:
            print("La cita no se encontró en la agenda.")

    def mover_cita(self, cita, nueva_fecha_hora):
        if self.verificar_disponibilidad(nueva_fecha_hora):
            cita.fecha_hora = nueva_fecha_hora
            print(f"Cita movida a {nueva_fecha_hora} para {cita.paciente.nombre}.")
            cita.notificar_cambio()
        else:
            print(f"No se puede mover la cita, el horario {nueva_fecha_hora} no está disponible.")