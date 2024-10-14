from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich import box
from datetime import datetime
from hospital import Hospital
from persona_factory import PersonasFactory
from app.paciente import Paciente
from app.medico import Medico
from app.cita import Cita

# Instancia de consola de Rich
console = Console()

hospital = Hospital.get_instance()

# Cargar los datos iniciales desde archivos
pacientes = Paciente.cargar_pacientes('pacientes.csv')
medicos = Medico.cargar_medicos('medicos.json')
citas = Cita.cargar_citas('citas.csv', pacientes, medicos)

def mostrar_menu():
    """Muestra el menú principal con Rich"""
    console.print(Panel("Bienvenido al sistema de gestión de citas médicas", title="Sistema de Citas Médicas", box=box.ROUNDED, style="bold blue"))
    table = Table(title="Menú Principal", show_header=True, header_style="bold magenta")
    table.add_column("Opción", style="cyan", justify="center")
    table.add_column("Descripción", style="green")

    table.add_row("1", "Agregar persona")
    table.add_row("2", "Pedir cita")
    table.add_row("3", "Cancelar cita")
    table.add_row("4", "Asignar médico de preferencia")
    table.add_row("5", "Ver citas pendientes")
    table.add_row("6", "Mover citas")
    table.add_row("7", "Salir")

    console.print(table)

def capturar_datos_persona():
    tipo_persona = Prompt.ask("Ingrese el tipo de persona (médico o paciente)").strip().lower()
    identificacion = Prompt.ask("Ingrese la identificación").strip()
    nombre = Prompt.ask("Ingrese el nombre").strip()
    correo = Prompt.ask("Ingrese el correo").strip()
    celular = Prompt.ask("Ingrese el celular").strip()
    whatsapp = Prompt.ask("Ingrese el WhatsApp (opcional)", default=None).strip()

    if tipo_persona == "medico":
        especialidad = Prompt.ask("Ingrese la especialidad").strip()
        persona = PersonasFactory.crear_persona(
            tipo="medico",
            identificacion=identificacion,
            nombre=nombre,
            correo=correo,
            celular=celular,
            especialidad=especialidad,
            whatsapp=whatsapp
        )
        hospital.agregar_medico(persona)
        console.print(f"[green]Médico {nombre} agregado exitosamente[/green]")
    elif tipo_persona == "paciente":
        persona = PersonasFactory.crear_persona(
            tipo="paciente",
            identificacion=identificacion,
            nombre=nombre,
            correo=correo,
            celular=celular,
            whatsapp=whatsapp
        )
        hospital.agregar_paciente(persona)
        console.print(f"[green]Paciente {nombre} agregado exitosamente[/green]")
    else:
        console.print("[red]Tipo de persona inválido[/red]")

def pedir_cita():
    id_paciente = Prompt.ask("Ingrese la identificación del paciente").strip()
    especialidad = Prompt.ask("Ingrese la especialidad requerida").strip()
    fecha = Prompt.ask("Ingrese la fecha de la cita (YYYY-MM-DD HH:MM)").strip()

    try:
        fecha_hora = datetime.strptime(fecha, "%Y-%m-%d %H:%M")
    except ValueError:
        console.print("[red]Formato de fecha/hora inválido[/red]")
        return

    paciente = hospital.buscar_paciente(id_paciente)
    if not paciente:
        console.print("[red]Paciente no encontrado[/red]")
        return

    id_medico_preferido = Prompt.ask("Ingrese la identificación del médico preferido (opcional)", default=None).strip()
    medico_preferido = hospital.buscar_medico(id_medico_preferido) if id_medico_preferido else None

    hospital.asignar_cita(paciente, especialidad, fecha_hora, medico_preferido)
    console.print(f"[green]Cita agendada exitosamente para {paciente.nombre}[/green]")

def cancelar_cita():
    id_paciente = Prompt.ask("Ingrese la identificación del paciente").strip()
    paciente = hospital.buscar_paciente(id_paciente)

    if paciente:
        citas_pendientes = hospital.buscar_cita(paciente=paciente)
        if citas_pendientes:
            table = Table(title="Citas Pendientes", show_header=True, header_style="bold magenta")
            table.add_column("Opción", style="cyan", justify="center")
            table.add_column("Descripción", style="green")

            for i, cita in enumerate(citas_pendientes, start=1):
                table.add_row(str(i), str(cita))

            console.print(table)

            try:
                opcion_cita = int(Prompt.ask("Seleccione la cita a cancelar").strip())
                if 1 <= opcion_cita <= len(citas_pendientes):
                    cita_a_cancelar = citas_pendientes[opcion_cita - 1]
                    hospital.cancelar_cita(paciente, cita_a_cancelar.medico, cita_a_cancelar.fecha_hora)
                    console.print("[green]Cita cancelada exitosamente[/green]")
                else:
                    console.print("[red]Opción inválida[/red]")
            except ValueError:
                console.print("[red]Entrada inválida. Por favor, ingrese un número[/red]")
        else:
            console.print(f"[yellow]No se encontraron citas pendientes para {paciente.nombre}[/yellow]")
    else:
        console.print("[red]Paciente no encontrado[/red]")

def main_menu():
    while True:
        mostrar_menu()
        opcion = Prompt.ask("Seleccione una opción").strip()

        if opcion == "1":
            capturar_datos_persona()
        elif opcion == "2":
            pedir_cita()
        elif opcion == "3":
            cancelar_cita()
        elif opcion == "4":
            id_paciente = Prompt.ask("Ingrese la identificación del paciente").strip()
            id_medico = Prompt.ask("Ingrese la identificación del médico").strip()

            paciente = hospital.buscar_paciente(id_paciente)
            medico = hospital.buscar_medico(id_medico)

            if paciente and medico:
                paciente.asignar_medico_preferencia(medico)
                console.print(f"[green]El Dr. {medico.nombre} ha sido asignado como médico de preferencia para {paciente.nombre}[/green]")
            else:
                console.print("[red]Paciente o médico no encontrado[/red]")
        elif opcion == "5":
            id_paciente = Prompt.ask("Ingrese la identificación del paciente").strip()
            paciente = hospital.buscar_paciente(id_paciente)

            if paciente:
                citas_pendientes = hospital.buscar_cita(paciente=paciente)
                if citas_pendientes:
                    table = Table(title="Citas Pendientes", show_header=True, header_style="bold magenta")
                    table.add_column("Descripción", style="green")
                    for cita in citas_pendientes:
                        table.add_row(str(cita))
                    console.print(table)
                else:
                    console.print(f"[yellow]No se encontraron citas pendientes para {paciente.nombre}[/yellow]")
            else:
                console.print("[red]Paciente no encontrado[/red]")
        elif opcion == "6":
            id_paciente = Prompt.ask("Ingrese la identificación del paciente").strip()
            id_medico = Prompt.ask("Ingrese la identificación del médico").strip()
            fecha_actual = Prompt.ask("Ingrese la fecha actual de la cita (YYYY-MM-DD HH:MM)").strip()
            nueva_fecha = Prompt.ask("Ingrese la nueva fecha para la cita (YYYY-MM-DD HH:MM)").strip()

            try:
                fecha_hora_actual = datetime.strptime(fecha_actual, "%Y-%m-%d %H:%M")
                nueva_fecha_hora = datetime.strptime(nueva_fecha, "%Y-%m-%d %H:%M")
            except ValueError:
                console.print("[red]Formato de fecha/hora inválido[/red]")
                continue

            paciente = hospital.buscar_paciente(id_paciente)
            medico = hospital.buscar_medico(id_medico)

            if paciente and medico:
                hospital.mover_cita(paciente, medico, fecha_hora_actual, nueva_fecha_hora)
                console.print("[green]Cita movida exitosamente[/green]")
            else:
                console.print("[red]Paciente o médico no encontrado[/red]")
        elif opcion == "7":
            console.print("[blue]Saliendo del programa...[/blue]")
            break
        else:
            console.print("[red]Opción inválida[/red]")

if __name__ == "__main__":
    main_menu()
