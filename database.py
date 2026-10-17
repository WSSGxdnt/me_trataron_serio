
import json
import aiofiles
import asyncio

ARCHIVO_BD = "inventario.json"
db_lock = asyncio.Lock()


async def leer_base_datos():
    try:
        async with aiofiles.open(
            ARCHIVO_BD, mode="r", encoding="utf-8"
        ) as f:
            contenido = await f.read()

            if not contenido.strip():
                return []

            return json.loads(contenido)

    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


async def guardar_base_datos(datos):
    async with aiofiles.open(
        ARCHIVO_BD, mode="w", encoding="utf-8"
    ) as f:
        await f.write(json.dumps(datos, indent=4, ensure_ascii=False))


async def crear_producto(codigo, nombre, stock):
    await asyncio.sleep(0.5)

    async with db_lock:
        datos = await leer_base_datos()

        for dato in datos:
            if dato["codigo"] == codigo:
                raise ValueError(
                    f"El producto con código {codigo} ya existe."
                )

        nuevo_producto = {
            "codigo": codigo,
            "nombre": nombre,
            "stock": stock
        }

        datos.append(nuevo_producto)
        await guardar_base_datos(datos)

        return nuevo_producto


async def obtener_producto(codigo):
    await asyncio.sleep(0.2)

    async with db_lock:
        datos = await leer_base_datos()

        for dato in datos:
            if dato["codigo"] == codigo:
                return dato.copy()

    raise KeyError(f"El producto {codigo} no ha sido encontrado xdnt.")


async def actualizar_stock(nuevo_stock, codigo):
    await asyncio.sleep(0.5)

    async with db_lock:
        datos = await leer_base_datos()

        for dato in datos:
            if dato["codigo"] == codigo:
                dato["stock"] = nuevo_stock
                await guardar_base_datos(datos)
                return dato.copy()

    raise KeyError(f"El producto {codigo} no ha sido encontrado :c.")


async def eliminar_producto(codigo):
    await asyncio.sleep(0.5)

    async with db_lock:
        datos = await leer_base_datos()

        nuevos_datos = [
            dato for dato in datos
            if dato["codigo"] != codigo
        ]

        if len(datos) == len(nuevos_datos):
            raise KeyError(
                f"El producto {codigo} no ha sido encontrado xdnt."
            )

        await guardar_base_datos(nuevos_datos)

    return True


async def alerta_stock_bajo(nombre, stock):
    if stock <= 2:
        await asyncio.sleep(0)
        print(
            f"ALERTA: El producto '{nombre}' "
            f"tiene solamente {stock} unidades."
        )


async def vender_producto(codigo, cantidad):
    if cantidad <= 0:
        raise ValueError("La cantidad a vender debe ser mayor que cero.")

    await asyncio.sleep(0.2)

    async with db_lock:
        datos = await leer_base_datos()

        for producto in datos:
            if producto["codigo"] == codigo:
                if producto["stock"] < cantidad:
                    raise ValueError(
                        f"Stock insuficiente para '{producto['nombre']}'. "
                        f"Disponible: {producto['stock']}, "
                        f"solicitado: {cantidad}."
                    )

                producto["stock"] -= cantidad
                resultado = producto.copy()
                await guardar_base_datos(datos)
                break
        else:
            raise KeyError(
                f"El producto {codigo} no ha sido encontrado."
            )

    # La alerta se ejecuta en segundo plano.
    asyncio.create_task(
        alerta_stock_bajo(resultado["nombre"], resultado["stock"])
    )

    return resultado
