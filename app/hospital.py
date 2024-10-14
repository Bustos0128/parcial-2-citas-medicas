from datetime import datetime, timedelta
from cita import Cita
from persona import Persona

class Hospital:
    __instance = None

    @staticmethod
    def get_instance():
        if Hospital.__instance is None:
            Hospital()
        return Hospital.__instance

    def __init__(self):
        if Hospital.__instance is not None:
            raise Exception(" ")
        else:
            self.pacientes = []
            self.medicos = []
            Hospital.__instance = self

    def agregar_paciente(self, paciente: Persona):
        self.pacientes.append(paciente)
        print(f"Paciente {paciente.nombre} agregado al hospital.")

    def agregar_medico(self, medico: Persona):
        self.medicos.append(medico)
        print(f"Médico {medico.nombre} agregado al hospital.")
        
    def buscar_paciente(self, identificacion=None, nombre=None):
        for paciente in self.pacientes:
            if identificacion and paciente.identificacion == identificacion:
                return paciente
            elif nombre and paciente.nombre.lower() == nombre.lower():
                return paciente
        return None  # No se encontró el paciente

    def buscar_medico(self, identificacion=None, nombre=None, especialidad=None):
        for medico in self.medicos:
            if identificacion and medico.identificacion == identificacion:
                return medico
            elif nombre and medico.nombre.lower() == nombre.lower():
                return medico
            elif especialidad and medico.especialidad.lower() == especialidad.lower():
                return medico
        return None  # No se encontró el médico

    def verificar_disponibilidad(self, especialidad, fecha_hora):
        for medico in self.medicos:
            if medico.especialidad.lower() == especialidad.lower() and medico.verificar_disponibilidad(fecha_hora):
                return medico
        print(f"No se encontró disponibilidad para la especialidad {especialidad}.")
        return None

    def asignar_cita(self, paciente, especialidad, fecha_hora, medico_preferido=None):
        medico_asignado = None

        if medico_preferido and medico_preferido.verificar_disponibilidad(fecha_hora):
            medico_asignado = medico_preferido
        else:
            medico_asignado = self.verificar_disponibilidad(especialidad, fecha_hora)

        if medico_asignado:
            nueva_cita = Cita(paciente, medico_asignado, fecha_hora)
            medico_asignado.agenda.agregar_cita(nueva_cita)
            print(f"Cita asignada con el Dr. {medico_asignado.nombre} para el paciente {paciente.nombre} el {fecha_hora}")
        else:
            print(f"No hay disponibilidad para la especialidad {especialidad} en la fecha {fecha_hora}")
            
    def cancelar_cita(self, paciente, medico, fecha_hora):
        cita_a_cancelar = next((c for c in medico.agenda.citas_pendientes if c.paciente == paciente and c.fecha_hora == fecha_hora), None)
        
        if cita_a_cancelar:
            medico.agenda.cancelar_cita(cita_a_cancelar)  # Interacción con la agenda del médico
            print(f"Cita cancelada para {paciente.nombre} con el Dr. {medico.nombre} el {fecha_hora}")
        else:
            print(f"No se encontró la cita para {paciente.nombre} con el Dr. {medico.nombre} el {fecha_hora}.")

    def enviar_recordatorios(self):
        """
        Envía recordatorios de citas programadas para dentro de dos días.
        """
        hoy = datetime.now()
        en_dos_dias = hoy + timedelta(days=2)
        for medico in self.medicos:
            for cita in medico.agenda.citas_pendientes:
                if cita.fecha_hora.date() == en_dos_dias.date():
                    cita.recordatorio_cita()
                    
    def buscar_cita(self, paciente=None, medico=None, fecha_hora=None):
        citas_encontradas = []
        if paciente:
            citas_encontradas = [c for c in paciente.medico.agenda.citas_pendientes if paciente == c.paciente]
        
        if medico:
            citas_encontradas = [c for c in medico.agenda.citas_pendientes if (not fecha_hora or c.fecha_hora == fecha_hora)]
        
        if fecha_hora and not paciente and not medico:
            for medico in self.medicos:
                citas_encontradas.extend([c for c in medico.agenda.citas_pendientes if c.fecha_hora == fecha_hora])
        
        return citas_encontradas
    
    def mover_cita(self, paciente, medico, fecha_hora_actual, nueva_fecha_hora):
        # Buscar la cita a mover
        cita_a_mover = next((c for c in medico.agenda.citas_pendientes if c.paciente == paciente and c.fecha_hora == fecha_hora_actual), None)

        if cita_a_mover:
            medico.agenda.mover_cita(cita_a_mover, nueva_fecha_hora)
        else:
            print(f"No se encontró la cita de {paciente.nombre} con el Dr. {medico.nombre} en la fecha {fecha_hora_actual}.")