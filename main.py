import asyncio
from database import crear_producto, obtener_producto, actualizar_stock, eliminar_producto
# from database import leer_base_datos, guardar_base_datos

# async def iniciar_sistema():
#     print("iniciando sistema")
#     datos = await leer_base_datos()
#     print(f"base de datos cargada con: {len(datos)}")

async def prueba_de_estres():
    print("-- iniciando prueba --")
    tareas_creacion = [
        crear_producto("M001", "llanta trasera", 10),
        crear_producto("M002", "filtro de aire", 25),
        crear_producto("M003", "bruja", 50),
    ]

    try:
        await asyncio.gather(*tareas_creacion)
        print("producto creados exitosamente")

    except Exception as e:
        print(f"error de creacion {e}")

    print("\nActualizar y consultar")
    try:
        resultado = await asyncio.gather(
            actualizar_stock(8, "M001"),
            obtener_producto("M002")
        )
        print("operaciones mixtas completadas")
        print(f" - update devolvio {resultado[0]}")