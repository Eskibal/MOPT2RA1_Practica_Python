import csv
import json
import os
import shutil
from typing import List

class RegistroHorario:
    def __init__(self, empleado: str, dia: str, entrada: int, salida: int):
        self.empleado = empleado
        self.dia = dia
        self.entrada = entrada
        self.salida = salida

    def duracion(self) -> int:
        """Devuelve la cantidad de horas trabajadas en este registro"""
        return self.salida - self.entrada

    def to_dict(self) -> dict:
        return {
            'empleado': self.empleado,
            'dia': self.dia,
            'entrada': self.entrada,
            'salida': self.salida,
            'duracion': self.duracion()
        }

CSV_PATH = 'horarios.csv'
registros: List[RegistroHorario] = []

def leer_csv(path: str) -> List[RegistroHorario]:
    registros_local: List[RegistroHorario] = []
    try:
        with open(path, newline='', encoding='utf-8') as f:
            first_line = f.readline()
            f.seek(0)
            has_header = ',' in first_line or ';' in first_line and any(h.lower() in first_line.lower() for h in ['empleado','nombre','dia','entrada','salida'])
            if has_header:
                lector = csv.DictReader(f, delimiter=';', quotechar='"')
                for fila in lector:
                    try:
                        nombre = fila.get('empleado') or fila.get('nombre') or fila.get('nombre_empleado') or ''
                        dia = fila.get('dia') or ''
                        entrada = int(fila.get('entrada') or fila.get('h_entrada') or fila.get('hora_entrada') or 0)
                        salida = int(fila.get('salida') or fila.get('h_salida') or fila.get('hora_salida') or 0)
                    except (ValueError, TypeError):
                        continue
                    registros_local.append(RegistroHorario(nombre, dia, entrada, salida))
            else:
                lector = csv.reader(f, delimiter=';', quotechar='"')
                for fila in lector:
                    if not fila:
                        continue
                    try:
                        nombre, dia, h_entrada, h_salida = fila
                        entrada = int(h_entrada)
                        salida = int(h_salida)
                    except ValueError:
                        continue
                    registros_local.append(RegistroHorario(nombre, dia, entrada, salida))
    except FileNotFoundError:
        print(f"Advertencia: no se encontró el archivo {path}. Empezando con lista vacía.")
    except IOError as e:
        print(f"Error de E/S al leer {path}: {e}")
    return registros_local

def guardar_csv(path: str, registros_list: List[RegistroHorario]) -> None:
    """Sobrescribe un CSV con los registros actuales"""
    tmp = path + '.tmp'
    try:
        with open(tmp, 'w', newline='', encoding='utf-8') as f:
            campos = ['empleado','dia','entrada','salida']
            escritor = csv.DictWriter(f, fieldnames=campos, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            escritor.writeheader()
            for r in registros_list:
                escritor.writerow({
                    'empleado': r.empleado,
                    'dia': r.dia,
                    'entrada': r.entrada,
                    'salida': r.salida
                })
        shutil.move(tmp, path)
    except IOError as e:
        print(f"Error al guardar CSV: {e}")
        if os.path.exists(tmp):
            os.remove(tmp)

def exportar_json(path: str, registros_list: List[RegistroHorario]) -> None:
    datos = [r.to_dict() for r in registros_list]
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error al guardar JSON: {e}")

registros = leer_csv(CSV_PATH)
print(f"Se han leído {len(registros)} registros desde {CSV_PATH}")

horarios = {
    'María':  ('08', '16'),
    'Juan':   ('09', '17'),
    'Lucía':  ('07', '15'),
    'Diego':  ('10', '18'),
    'Ana':    ('08', '14'),
    'Raúl':   ('12', '20'),
}

def mostrar_registros():
    """Muestra primero los registros leídos desde CSV y luego el diccionario estático"""
    print("Registros leídos desde CSV:")
    if registros:
        for i, r in enumerate(registros, start=0):
            print(f"{i}: {r.empleado} - {r.dia} (Entrada: {r.entrada}h - Salida: {r.salida}h) Duración: {r.duracion()}h")
    else:
        print("No hay registros leídos desde CSV.")
    print("\nHorarios estáticos:")
    for i, (nombre, (entrada, salida)) in enumerate(horarios.items(), start=0):
        print(f"{i}: {nombre} (Entrada: {entrada}h - Salida: {salida}h)")
    print()

def contar_entradas():
    try:
        hora = int(input("Introduce una hora (0-23): ").strip())
    except ValueError:
        print("Hora no válida.")
        return

    cont = 0
    for nombre, (entrada, _) in horarios.items():
        try:
            if int(entrada) <= hora:
                cont += 1
        except ValueError:
            continue

    cont_registros = sum(1 for r in registros if r.entrada <= hora)
    print(f"\n{cont} empleados (diccionario estático) han llegado antes o a las {hora}h")
    print(f"{cont_registros} registros (CSV) tienen entrada <= {hora}h")

def anadir_registro_interactivo():
    nombre = input("Empleado: ").strip()
    dia = input("Día: ").strip()
    try:
        entrada = int(input("Hora entrada (0-23): ").strip())
        salida = int(input("Hora salida (0-23): ").strip())
    except ValueError:
        print("Horas inválidas. Operación cancelada.")
        return
    if not (0 <= entrada <= 23 and 0 <= salida <= 23 and salida >= entrada):
        print("Rango de horas inválido. Operación cancelada.")
        return
    nuevo = RegistroHorario(nombre, dia, entrada, salida)
    registros.append(nuevo)
    print("Registro añadido en memoria. Para persistir llame a 'guardar' desde el menú.")

def eliminar_archivo(path: str):
    if not os.path.exists(path):
        print(f"No existe {path}")
        return
    try:
        os.remove(path)
        print(f"{path} eliminado.")
    except PermissionError:
        print("Permiso denegado al intentar eliminar el archivo.")
    except OSError as e:
        print(f"Error al eliminar {path}: {e}")

def renombrar_archivo(old: str, new: str):
    if not os.path.exists(old):
        print(f"No existe {old}")
        return
    try:
        os.rename(old, new)
        print(f"{old} renombrado a {new}")
    except OSError as e:
        print(f"Error al renombrar: {e}")

def menu():
    while True:
        print("========== MENÚ ==========")
        print("1) Mostrar registros")
        print("2) Contar entradas")
        print("3) Añadir registro (en memoria)")
        print("4) Guardar registros en CSV")
        print("5) Exportar registros a JSON")
        print("6) Eliminar archivo CSV")
        print("7) Renombrar archivo CSV")
        print("8) Salir")
        opcion = input("Elige una opción (1-8): ").strip()

        if opcion == '1':
            mostrar_registros()
        elif opcion == '2':
            contar_entradas()
        elif opcion == '3':
            anadir_registro_interactivo()
        elif opcion == '4':
            guardar_csv(CSV_PATH, registros)
            print(f"Registros guardados en {CSV_PATH}")
        elif opcion == '5':
            exportar_json('horarios.json', registros)
            print("Exportado a horarios.json")
        elif opcion == '6':
            eliminar_archivo(CSV_PATH)
        elif opcion == '7':
            nuevo_nombre = input("Nuevo nombre para el CSV: ").strip()
            if nuevo_nombre:
                renombrar_archivo(CSV_PATH, nuevo_nombre)
        elif opcion == '8':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.\n")

# ---------------------------------------------------------------------------
#  Punto de entrada
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    menu()
