# migrar_desde_excel.py
"""
Migrar datos desde archivos Excel descargados de Google Sheets
a la base de datos PostgreSQL (emporio_teo).

Archivos esperados en la raíz:
- Inventario_Emporio_Teo.xlsx
- Gastos_Emporio_Teo.xlsx
- Ventas_Emporio_Teo.xlsx

Este script está pensado para ejecutarse MÁS DE UNA VEZ sin duplicar
gastos ni ventas, y sin duplicar inventario (lo actualiza por código).
"""

import pandas as pd
from datetime import datetime, date
from app.db.session import SessionLocal
from app.models.inventario import Inventario
from app.models.gastos import Gasto
from app.models.ventas import Venta

db = SessionLocal()


def parse_fecha(valor):
    if pd.isna(valor):
        return date.today()
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    texto = str(valor).strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(texto, fmt).date()
        except ValueError:
            continue
    return date.today()


def parse_hora(valor):
    if pd.isna(valor):
        return datetime.now().time()
    if isinstance(valor, datetime):
        return valor.time()
    texto = str(valor).strip()
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(texto, fmt).time()
        except ValueError:
            continue
    return datetime.now().time()


def migrar_inventario():
    try:
        df = pd.read_excel("Inventario_Emporio_Teo.xlsx")
    except FileNotFoundError:
        print("⚠️ No se encontró Inventario_Emporio_Teo.xlsx, se salta inventario.")
        return

    # normalizamos nombres de columnas
    df.columns = [c.strip().lower() for c in df.columns]

    for _, fila in df.iterrows():
        codigo = str(fila.get("codigo") or "").strip()
        if not codigo:
            continue

        nombre = fila.get("nombre") or ""
        precio = float(fila.get("precio") or 0)
        precio_costo = float(fila.get("precio_costo") or 0)
        cantidad = int(fila.get("cantidad") or 0)
        stock_estado = fila.get("stock_estado") or ""

        existente = db.query(Inventario).filter(Inventario.codigo == codigo).first()

        if existente:
            # actualizamos datos por si cambiaron en el Excel
            existente.nombre = nombre
            existente.precio = precio
            existente.precio_costo = precio_costo
            existente.cantidad = cantidad
            existente.stock_estado = stock_estado
            db.add(existente)
        else:
            db.add(
                Inventario(
                    codigo=codigo,
                    nombre=nombre,
                    precio=precio,
                    precio_costo=precio_costo,
                    cantidad=cantidad,
                    stock_estado=stock_estado,
                )
            )

    db.commit()
    print("✅ Inventario migrado/actualizado desde Excel")


def migrar_gastos():
    try:
        df = pd.read_excel("Gastos_Emporio_Teo.xlsx")
    except FileNotFoundError:
        print("⚠️ No se encontró Gastos_Emporio_Teo.xlsx, se salta gastos.")
        return

    df.columns = [c.strip().lower() for c in df.columns]

    insertados = 0
    saltados = 0

    for _, fila in df.iterrows():
        fecha = parse_fecha(fila.get("fecha"))
        comercio = (fila.get("comercio") or "").strip()
        detalle = (fila.get("detalle") or "").strip()
        monto = float(fila.get("monto") or 0)

        # control anti-duplicado
        existente = db.query(Gasto).filter(
            Gasto.fecha == fecha,
            Gasto.comercio == comercio,
            Gasto.detalle == detalle,
            Gasto.monto == monto,
        ).first()

        if existente:
            saltados += 1
            continue

        db.add(
            Gasto(
                fecha=fecha,
                comercio=comercio,
                detalle=detalle,
                monto=monto,
            )
        )
        insertados += 1

    db.commit()
    print(f"✅ Gastos migrados desde Excel (nuevos: {insertados}, repetidos: {saltados})")


def migrar_ventas():
    try:
        df = pd.read_excel("Ventas_Emporio_Teo.xlsx")
    except FileNotFoundError:
        print("⚠️ No se encontró Ventas_Emporio_Teo.xlsx, se salta ventas.")
        return

    df.columns = [c.strip().lower() for c in df.columns]

    insertadas = 0
    saltadas = 0

    for _, fila in df.iterrows():
        fecha = parse_fecha(fila.get("fecha"))
        hora = parse_hora(fila.get("hora"))
        total = float(fila.get("total") or 0)
        tipo_pago = (fila.get("tipo_pago") or "Efectivo").strip()

        # control anti-duplicado
        existente = db.query(Venta).filter(
            Venta.fecha == fecha,
            Venta.hora == hora,
            Venta.total == total,
            Venta.tipo_pago == tipo_pago,
        ).first()

        if existente:
            saltadas += 1
            continue

        db.add(
            Venta(
                fecha=fecha,
                hora=hora,
                total=total,
                tipo_pago=tipo_pago,
            )
        )
        insertadas += 1

    db.commit()
    print(f"✅ Ventas migradas desde Excel (nuevas: {insertadas}, repetidas: {saltadas})")


if __name__ == "__main__":
    migrar_inventario()
    migrar_gastos()
    migrar_ventas()
    db.close()
    print("🎉 Migración desde Excel completa")


