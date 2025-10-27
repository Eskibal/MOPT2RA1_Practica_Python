import csv
import os
from typing import List, Dict, Set

class RegistroHorario:
    def __init__(self, empleado: str, dia: str, entrada: int, salida: int):
        self.empleado = empleado.strip()
        self.dia = dia.strip()
        self.entrada = int(entrada)
        self.salida = int(salida)
    def duracion(self) -> int:
        return self.salida - self.entrada

class Empleado:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.registros: List[RegistroHorario] = []
    def agregar_registro(self, reg: RegistroHorario):
        if reg.empleado == self.nombre:
            self.registros.append(reg)
    def horas_totales(self) -> int:
        return sum(r.duracion() for r in self.registros)
    def dias_distintos(self) -> Set[str]:
        return {r.dia for r in self.registros}
    def fila_resumen(self):
        return [self.nombre, str(len(self.dias_distintos())), str(self.horas_totales())]

class GestorHorarios:
    def __init__(self, path='horarios.csv', delim=';'):
        self.path = path
        self.delim = delim
        self.registros: List[RegistroHorario] = []
        self.empleados: Dict[str, Empleado] = {}
        self.empleados_por_dia: Dict[str, Set[str]] = {}

    def leer_csv(self):
        self.registros.clear()
        if not os.path.exists(self.path):
            print(f"Archivo no encontrado: {self.path}")
            return
        with open(self.path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=self.delim, quotechar='"')
            first = next(reader, None)
            if first is None:
                return
            header_like = any(h.lower() in ('nombre_empleado','empleado','dia','hora_entrada','hora_salida') for h in first)
            rows = reader if header_like else [first] + list(reader)
            for fila in rows:
                if not fila or len(fila) < 4:
                    continue
                try:
                    nombre, dia, he, hs = fila[:4]
                    entrada, salida = int(he), int(hs)
                except ValueError:
                    continue
                self.registros.append(RegistroHorario(nombre, dia, entrada, salida))
        self._reconstruir()
        print(f"Leídos {len(self.registros)} registros desde {self.path}")

    def _reconstruir(self):
        self.empleados.clear()
        self.empleados_por_dia.clear()
        for r in self.registros:
            if r.empleado not in self.empleados:
                self.empleados[r.empleado] = Empleado(r.empleado)
            self.empleados[r.empleado].agregar_registro(r)
            self.empleados_por_dia.setdefault(r.dia, set()).add(r.empleado)

    def escribir_resumen_horarios(self, salida='resumen_horarios.csv'):
        horas = {n: e.horas_totales() for n, e in self.empleados.items()}
        with open(salida, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f, delimiter=self.delim, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(['Empleado', 'Horas totales'])
            for nombre, total in sorted(horas.items()):
                w.writerow([nombre, total])
        print(f"Generado {salida}")

    def escribir_resumen_semanal(self, salida='resumen_semanal.csv'):
        with open(salida, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f, delimiter=self.delim, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(['Empleado', 'Dias_trabajados', 'Horas_totales'])
            for nombre, emp in sorted(self.empleados.items()):
                w.writerow(emp.fila_resumen())
        print(f"Generado {salida}")

    def escribir_madrugadores(self, hora_ref=8, salida='madrugadores.csv'):
        minimo: Dict[str, int] = {}
        for r in self.registros:
            minimo[r.empleado] = min(minimo.get(r.empleado, 24), r.entrada)
        madrugadores = {e: h for e, h in minimo.items() if h < hora_ref}
        with open(salida, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f, delimiter=self.delim, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(['Empleado', 'Hora_entrada'])
            for nombre, hora in sorted(madrugadores.items()):
                w.writerow([nombre, hora])
        print(f"Generado {salida}")

    def mostrar_resumen_console(self):
        print(f"\nRegistros: {len(self.registros)}")
        print(f"Empleados: {len(self.empleados)}")
        print(f"Días detectados: {sorted(self.empleados_por_dia.keys())}")
        print("Horas por empleado:")
        for nombre, emp in sorted(self.empleados.items()):
            print(f"  {nombre}: {emp.horas_totales()}h en {len(emp.dias_distintos())} días")

# Menú reducido
def menu_reducido():
    gestor = GestorHorarios()
    while True:
        print("\n--- MENÚ REDUCIDO ---")
        print("1) Cargar horarios desde CSV")
        print("2) Mostrar resumen en pantalla")
        print("3) Generar archivos: resumen_horarios.csv y resumen_semanal.csv")
        print("4) Generar madrugadores.csv (por defecto < 8h)")
        print("5) Añadir registro rápido (memoria)")
        print("0) Salir")
        op = input("Elige opción: ").strip()
        if op == '1':
            gestor.leer_csv()
        elif op == '2':
            gestor.mostrar_resumen_console()
        elif op == '3':
            gestor.escribir_resumen_horarios()
            gestor.escribir_resumen_semanal()
        elif op == '4':
            try:
                hr = int(input("Hora referencia (por defecto 8): ").strip() or "8")
            except ValueError:
                hr = 8
            gestor.escribir_madrugadores(hora_ref=hr)
        elif op == '5':
            nombre = input("Nombre: ").strip()
            dia = input("Día: ").strip()
            try:
                entrada = int(input("Entrada (0-23): ").strip())
                salida = int(input("Salida (0-23): ").strip())
            except ValueError:
                print("Horas inválidas. Registro no añadido.")
                continue
            gestor.registros.append(RegistroHorario(nombre, dia, entrada, salida))
            gestor._reconstruir()
            print("Registro añadido en memoria.")
        elif op == '0':
            print("Saliendo.")
            break
        else:
            print("Opción no válida.")

if __name__ == '__main__':
    menu_reducido()
