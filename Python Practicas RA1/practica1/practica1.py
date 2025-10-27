empleados = int(input("Introduce num. empleados: "))
hora_referencia = int(input("Hora de referencia (0-23): "))

cont = 0
contador_entradas = 0
salida_mas_temprana = 0
nombre_salida_temprana = ""

while cont < empleados:
    nombre_empleado = input("\nIntroduce nombre empleado: ")
    hora_entrada = int(input("Hora de entrada (0-23): "))
    hora_salida = int(input("Hora de salida (0-23): "))

    if hora_entrada < 0 or hora_entrada > 23 or hora_salida < 0 or hora_salida > 23 :
        print("Error: Las horas deben estar entre 0 y 23")
        continue
    elif hora_salida <= hora_entrada :
        print("Error: La hora de salida debe ser mayor que la de entrada")
        continue

    if hora_entrada <= hora_referencia :
        contador_entradas += 1

    if hora_salida >= hora_referencia :
        salida_mas_temprana = hora_salida
        nombre_salida_temprana = nombre_empleado

    cont += 1

print("\nResultado >")
print("Empleados que entraron antes o a la hora de referencia:", contador_entradas)
if nombre_salida_temprana != "" :
    print("El empleado", nombre_salida_temprana, "ha salido antes a las", salida_mas_temprana)
else :
     print("No se registro ninguna salida valida.")

    