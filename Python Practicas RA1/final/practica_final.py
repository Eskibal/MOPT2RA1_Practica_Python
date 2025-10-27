import csv
import re
from datetime import datetime

# -------------------- CLASES --------------------

class Cliente:
    def __init__(self, id, nombre, email, fecha_registro):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.fecha_registro = datetime.strptime(fecha_registro, "%Y-%m-%d")

    def antiguedad_dias(self):
        return (datetime.today().date() - self.fecha_registro.date()).days

    def __str__(self):
        return f"{self.id} - {self.nombre} ({self.email})"

class Evento:
    def __init__(self, id, nombre, categoria, fecha, precio):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.fecha = datetime.strptime(fecha, "%Y-%m-%d")
        self.precio = float(precio)

    def dias_hasta_evento(self):
        return (self.fecha.date() - datetime.today().date()).days

    def __str__(self):
        return f"{self.id} - {self.nombre} ({self.categoria})"

class Venta:
    def __init__(self, id, cliente_id, evento_id, fecha, precio):
        self.id = id
        self.cliente_id = cliente_id
        self.evento_id = evento_id
        self.fecha = datetime.strptime(fecha, "%Y-%m-%d")
        self.precio = float(precio)

    def __str__(self):
        return f"{self.id} - Cliente: {self.cliente_id}, Evento: {self.evento_id}, Precio: {self.precio}"

# -------------------- FUNCIONES --------------------

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validar_fecha(fecha_str):
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d")
    except ValueError:
        return None

def cargar_datos():
    clientes, eventos, ventas = {}, {}, []

    try:
        with open("data/clientes.csv", newline='') as f:
            for row in csv.DictReader(f):
                cliente = Cliente(**row)
                clientes[cliente.id] = cliente
    except FileNotFoundError:
        print("Archivo clientes.csv no encontrado.")

    try:
        with open("data/eventos.csv", newline='') as f:
            for row in csv.DictReader(f):
                evento = Evento(**row)
                eventos[evento.id] = evento
    except FileNotFoundError:
        print("Archivo eventos.csv no encontrado.")

    try:
        with open("data/ventas.csv", newline='') as f:
            for row in csv.DictReader(f):
                venta = Venta(**row)
                ventas.append(venta)
    except FileNotFoundError:
        print("Archivo ventas.csv no encontrado.")

    return clientes, eventos, ventas

def guardar_cliente(cliente):
    with open("data/clientes.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([cliente.id, cliente.nombre, cliente.email, cliente.fecha_registro.strftime("%Y-%m-%d")])

def exportar_informe(ventas):
    ingresos = {}
    for v in ventas:
        ingresos[v.evento_id] = ingresos.get(v.evento_id, 0) + v.precio
    with open("data/informe_resumen.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Evento ID", "Ingresos Totales"])
        for eid, total in ingresos.items():
            writer.writerow([eid, total])
    print("Informe exportado correctamente.")

# -------------------- MENÚ --------------------

def main():
    clientes, eventos, ventas = {}, {}, []

    while True:
        print("\n--- MINI CRM DE EVENTOS ---")
        print("1. Cargar CSV")
        print("2. Listar tablas")
        print("3. Alta de cliente")
        print("4. Filtrar ventas por rango de fechas")
        print("5. Estadísticas")
        print("6. Exportar informe")
        print("7. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            clientes, eventos, ventas = cargar_datos()
            print("Datos cargados correctamente.")

        elif opcion == "2":
            print("Clientes:")
            for c in clientes.values():
                print(c)
            print("\nEventos:")
            for e in eventos.values():
                print(e)
            print("\nVentas:")
            for v in ventas:
                print(v)

        elif opcion == "3":
            nombre = input("Nombre: ")
            email = input("Email: ")
            if not validar_email(email):
                print("Email inválido.")
                continue
            fecha = input("Fecha de registro (YYYY-MM-DD): ")
            fecha_valida = validar_fecha(fecha)
            if not fecha_valida:
                print("Fecha inválida.")
                continue
            nuevo_id = str(len(clientes) + 1)
            cliente = Cliente(nuevo_id, nombre, email, fecha)
            clientes[nuevo_id] = cliente
            guardar_cliente(cliente)
            print("Cliente añadido correctamente.")

        elif opcion == "4":
            f1 = input("Fecha inicio (YYYY-MM-DD): ")
            f2 = input("Fecha fin (YYYY-MM-DD): ")
            d1, d2 = validar_fecha(f1), validar_fecha(f2)
            if not d1 or not d2:
                print("Fechas inválidas.")
                continue
            filtradas = [v for v in ventas if d1 <= v.fecha <= d2]
            for v in filtradas:
                print(v)

        elif opcion == "5":
            total = sum(v.precio for v in ventas)
            ingresos_por_evento = {}
            categorias = set()
            precios = []

            for v in ventas:
                ingresos_por_evento[v.evento_id] = ingresos_por_evento.get(v.evento_id, 0) + v.precio
                precios.append(v.precio)
                if v.evento_id in eventos:
                    categorias.add(eventos[v.evento_id].categoria)

            dias_eventos = [e.dias_hasta_evento() for e in eventos.values()]
            resumen = (min(precios), max(precios), sum(precios)/len(precios)) if precios else (0, 0, 0)

            print(f"Ingresos totales: {total}")
            print("Ingresos por evento:", ingresos_por_evento)
            print("Categorías:", categorias)
            print("Días hasta evento más próximo:", min(dias_eventos))
            print("Resumen precios (min, max, media):", resumen)

        elif opcion == "6":
            exportar_informe(ventas)

        elif opcion == "7":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
