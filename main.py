import asyncio
from database import (
crear_producto, obtener_producto, actualizar_stock, eliminar_producto
)



async def realizar_venta(codigo, unidades, descripcion):
    print(f"\n[VENTAS S.A. o algo asi...] Iniciando operacion: {descripcion}")

    try:
        producto = await obtener_producto(codigo)

        if producto is None:
            raise ValueError(
                f"El producto {codigo} no existe >:c "
                "Alguien intenta vender aire."
            )
        
        stock_actual = producto[2]

        print(
            f"[VENTAS S.A. o no se...] {codigo}: "
            f"stock actual = {stock_actual}, "
            f"solicitado = {unidades}"
        )

        if unidades > stock_actual:
            raise ValueError(
                f"Stock insuficiente para {codigo}. "
                f"Hay {stock_actual}, pero piden {unidades}. "
                "Ni con milagros alcanza xd."
            )

        await actualizar_stock(-unidades, codigo)

        stock_restante = stock_actual - unidades

        print(
            f"[VENTAS S.A. xd] Venta completada: {descripcion}. "
            f"Quedan {stock_restante} unidades."
        )

        if stock_restante <= 2:
            asyncio.create_task(
                alerta_stock_bajo(codigo, stock_restante)
            )

        return f"Venta exitosa :D {codigo}"

    except ValueError as e:
        print(f"[VENTAS S.A.] Venta rechazada: {e}")
        return f"Venta fallida :c {codigo}"

    except Exception as e:
        print(
            f"[VENTAS S.A.] Error inesperado en {codigo}: {e}"
        )
        return f"Error inesperado: {codigo}"


async def alerta_stock_bajo(codigo, stock):
    # Simular que la alerta trabaja en segundo plano 7o7
    await asyncio.sleep(0.5)

    print(
        f"\n[ALERTA DE EMERGENCIA!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ok ya] Producto {codigo}: "
        f"solo quedan {stock} unidades. "
        "el almacen esta en modo supervivencia xd"
    )


async def prueba_de_estres():
    print("=" * 55)
    print(" VENTAS S.A. o no se xdxd - PRUEBA DE ESTRES DEL ALMACEN")
    print(" Cuatro ventas, cero ganas de contar tornillos.")
    print("=" * 55)

    # Crear productos de prueba
    tareas_creacion = [
        crear_producto("M001", "Llanta trasera", 20),
        crear_producto("M002", "Filtro de aire", 10),
        crear_producto("M003", "Bujia", 15),
        crear_producto("M004", "Aceite de motor", 5),
    ]

    try:
        await asyncio.gather(*tareas_creacion)
        print("\n[ALMACEN] Productos preparados para el caos.")
    except Exception as e:
        print(f"[ALMACEN] Error al preparar productos: {e}")
        return

    print("\n[CAJA REGISTRADORA] Abriendo cuatro cajas...")
    print("[CAJA REGISTRADORA] :v \n")

    # las 4 ventas simultaneas::
    tareas_ventas = [
        realizar_venta("M001", 5, "Venta normal de llantas"),
        realizar_venta("M002", 8, "Venta con stock critico"),
        realizar_venta("M003", 50, "Venta de unidades imaginarias"),
        realizar_venta("M004", 2, "Venta normal de aceite"),
    ]

    resultados = await asyncio.gather(*tareas_ventas)

    print("\n" + "=" * 55)
    print("[GERENCIA] Resumen de las cuatro ventas:")
    for resultado in resultados:
        print(f" - {resultado}")

    # Dar tiempo a las alertas en segundo plano para poder terminae
    await asyncio.sleep(0.6)

    print("\n[GERENCIA] Prueba terminada xd")
    print("[GERENCIA] El almacen sigue vivo :D")
    print("=" * 55)


asyncio.run(prueba_de_estres())