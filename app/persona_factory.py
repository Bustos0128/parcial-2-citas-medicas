from paciente import Paciente
from medico import Medico

class PersonasFactory:
    @staticmethod
    def crear_persona(tipo, identificacion, nombre, correo, celular, especialidad=None, whatsapp=None):
        if tipo.lower() == 'medico':
            return Medico(identificacion, nombre, correo, celular, especialidad, whatsapp)
        elif tipo.lower() == 'paciente':
            return Paciente(identificacion, nombre, correo, celular, whatsapp)
        else:
            raise ValueError(f"Tipo de persona desconocido: {tipo}")
