# Mini-CRM de Eventos — Resumen
Aplicación en Python que gestiona clientes, eventos y ventas usando archivos CSV. Funciona por consola y permite registrar clientes, filtrar ventas por fechas, calcular métricas y exportar informes.

## Objetivos
- Leer y escribir archivos CSV.
- Usar clases (`Cliente`, `Evento`, `Venta`) y colecciones (`list`, `dict`, `set`, `tuple`).
- Manejar fechas con `datetime`.
- Validar datos de entrada (email, fechas).
- Exportar métricas e informes.

## Estructura del proyecto
```
Final/
├── mini_crm.py # Código fuente principal
├── README.md # Este archivo
└── data/
├── clientes.csv # Datos de clientes
├── eventos.csv # Datos de eventos
├── ventas.csv # Datos de ventas
└── informe_resumen.csv # Informe generado por la app
```

## Funciones principales
- Menú interactivo
- Lectura/escritura de CSV
- Clases: `Cliente`, `Evento`, `Venta`
- Validación de email y fechas
- Estadísticas: ingresos, categorías, precios
- Exportación de informe resumen

