# app/web/routes.py  (añadir este bloque)

from datetime import date, datetime, timedelta
from collections import defaultdict

from fastapi import APIRouter, Depends, Query, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates

from app.db.session import get_db
from app.models.inventario import Inventario
from app.models.ventas import Venta
from app.models.gastos import Gasto
from app.core.deps import (get_current_active_user_from_cookie, get_current_admin_user_from_cookie)
from app.core.security import create_access_token
from app.core.config import settings
from app.services.usuario_service import UsuarioService

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

usuario_service = UsuarioService()


# =========================
# Menú principal
# =========================
@router.get("/panel", response_class=HTMLResponse)
def menu_principal(
    request: Request,
    current_user=Depends(get_current_active_user_from_cookie),
):
    """
    Menú principal del sistema web.
    Desde aquí se navega a inventario, ventas, gastos y reportes.
    """
    return templates.TemplateResponse(
        "menu_principal.html",
        {
            "request": request,
            "current_user": current_user,
        },
    )


# =========================
# Login / Logout
# =========================
@router.get("/panel/login", response_class=HTMLResponse)
def login_form(
    request: Request,
    error: str | None = None,
):
    """
    Muestra el formulario de login.
    """
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": error,
        },
    )


@router.post("/panel/login")
def login_submit(
    request: Request,
    db: Session = Depends(get_db),
    username: str = Form(...),
    password: str = Form(...),
    next: str | None = Form(default=None),
):
    usuario = usuario_service.autenticar(db, username=username, password=password)
    if not usuario:
        url = "/panel/login?error=Usuario+o+contraseña+incorrectos"
        return RedirectResponse(url=url, status_code=303)

    # Crear token JWT
    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.username, "role": usuario.role},
        expires_delta=expires,
    )

    # 🔥 SIEMPRE redirigir al menú principal
    redirect_url = "/panel"

    response = RedirectResponse(url=redirect_url, status_code=303)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False,  # Cambia a True en producción con HTTPS
        max_age=expires.total_seconds(),
    )
    return response


@router.get("/panel/logout")
def logout():
    """
    Cierra sesión:
    - elimina cookie 'access_token'
    - redirige al login
    """
    response = RedirectResponse(url="/panel/login", status_code=303)
    response.delete_cookie("access_token")
    return response


# =========================
# Panel de Inventario
# =========================
@router.get("/panel/inventario", response_class=HTMLResponse)
def ver_inventario_web(
    request: Request,
    db: Session = Depends(get_db),
    buscar: str = Query("", description="Buscar por nombre o código"),
    current_user=Depends(get_current_active_user_from_cookie),
):
    query = db.query(Inventario)

    if buscar:
        texto = f"%{buscar.lower()}%"
        query = query.filter(
            (Inventario.codigo.ilike(texto)) |
            (Inventario.nombre.ilike(texto))
        )

    items = query.order_by(Inventario.nombre).all()

    return templates.TemplateResponse(
        "inventario.html",
        {
            "request": request,
            "items": items,
            "buscar": buscar,
            "current_user": current_user,
        },
    )

# =========================
# Inventario - Nuevo producto (formulario)
# =========================
@router.get("/panel/inventario/nuevo", response_class=HTMLResponse)
def inventario_nuevo_form(
    request: Request,
    current_user=Depends(get_current_admin_user_from_cookie),
):
    """
    Muestra formulario para crear un nuevo producto.
    """
    return templates.TemplateResponse(
        "inventario_form.html",
        {
            "request": request,
            "modo": "nuevo",
            "producto": None,
            "current_user": current_user,
        },
    )


@router.post("/panel/inventario/nuevo")
def inventario_nuevo_guardar(
    request: Request,
    db: Session = Depends(get_db),
    codigo: str = Form(...),
    nombre: str = Form(...),
    precio: float = Form(...),
    precio_costo: float = Form(...),
    cantidad: int = Form(...),
    stock_estado: str = Form(""),
    current_user=Depends(get_current_admin_user_from_cookie),
):
    """
    Crea un nuevo producto en inventario.
    """
    nuevo = Inventario(
        codigo=codigo,
        nombre=nombre,
        precio=precio,
        precio_costo=precio_costo,
        cantidad=cantidad,
        stock_estado=stock_estado,
    )
    db.add(nuevo)
    db.commit()

    return RedirectResponse(url="/panel/inventario", status_code=303)


# =========================
# Inventario - Editar producto
# =========================
@router.get("/panel/inventario/editar/{producto_id}", response_class=HTMLResponse)
def inventario_editar_form(
    producto_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user_from_cookie),
):
    producto = db.query(Inventario).get(producto_id)
    if not producto:
        return RedirectResponse(url="/panel/inventario", status_code=303)

    return templates.TemplateResponse(
        "inventario_form.html",
        {
            "request": request,
            "modo": "editar",
            "producto": producto,
            "current_user": current_user,
        },
    )


@router.post("/panel/inventario/editar/{producto_id}")
def inventario_editar_guardar(
    producto_id: int,
    request: Request,
    db: Session = Depends(get_db),
    codigo: str = Form(...),
    nombre: str = Form(...),
    precio: float = Form(...),
    precio_costo: float = Form(...),
    cantidad: int = Form(...),
    stock_estado: str = Form(""),
    current_user=Depends(get_current_admin_user_from_cookie),
):
    producto = db.query(Inventario).get(producto_id)
    if not producto:
        return RedirectResponse(url="/panel/inventario", status_code=303)

    producto.codigo = codigo
    producto.nombre = nombre
    producto.precio = precio
    producto.precio_costo = precio_costo
    producto.cantidad = cantidad
    producto.stock_estado = stock_estado

    db.commit()

    return RedirectResponse(url="/panel/inventario", status_code=303)


# =========================
# Inventario - Desactivar producto
# =========================
@router.post("/panel/inventario/desactivar/{producto_id}")
def inventario_desactivar(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user_from_cookie),
):
    """
    Desactiva un producto marcándolo sin stock.
    (Aquí simplemente ponemos cantidad = 0 y stock_estado = 'DESACTIVADO').
    Ajusta esta lógica si quieres algo distinto.
    """
    producto = db.query(Inventario).get(producto_id)
    if producto:
        producto.cantidad = 0
        producto.stock_estado = "DESACTIVADO"
        db.commit()

    return RedirectResponse(url="/panel/inventario", status_code=303)



# =========================
# Panel de Ventas (listado por fecha)
# =========================
@router.get("/panel/ventas", response_class=HTMLResponse)
def ver_ventas_web(
    request: Request,
    db: Session = Depends(get_db),
    fecha: date = Query(default_factory=date.today),
    current_user=Depends(get_current_active_user_from_cookie),
):
    """Lista ventas de una fecha (por defecto, hoy)."""
    ventas = (
        db.query(Venta)
        .filter(Venta.fecha == fecha)
        .order_by(Venta.hora.desc())
        .all()
    )

    total_dia = sum(v.total for v in ventas) if ventas else 0

    return templates.TemplateResponse(
        "ventas.html",
        {
            "request": request,
            "ventas": ventas,
            "fecha": fecha,
            "total_dia": total_dia,
            "current_user": current_user,
        },
    )


# =========================
# Pantalla Registrar Venta (form + ventas del día)
# =========================
@router.get("/panel/ventas/nueva", response_class=HTMLResponse)
def nueva_venta_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user_from_cookie),
):
    """Formulario de nueva venta + listado de ventas de hoy."""
    hoy = date.today()

    ventas_hoy = (
        db.query(Venta)
        .filter(Venta.fecha == hoy)
        .order_by(Venta.hora.desc())
        .all()
    )

    total_dia = sum(v.total for v in ventas_hoy) if ventas_hoy else 0

    return templates.TemplateResponse(
        "venta_nueva.html",
        {
            "request": request,
            "fecha": hoy,
            "ventas": ventas_hoy,
            "total_dia": total_dia,
            "current_user": current_user,
        },
    )


@router.post("/panel/ventas/nueva")
def crear_venta_web(
    request: Request,
    db: Session = Depends(get_db),
    total: float = Form(...),
    tipo_pago: str = Form(...),
    current_user=Depends(get_current_active_user_from_cookie),
):
    """Crea una venta simple con fecha y hora actual y vuelve a la misma pantalla."""
    ahora = datetime.now()

    # Hora sin microsegundos
    hora_sin_micro = ahora.replace(microsecond=0).time()

    nueva = Venta(
        fecha=ahora.date(),
        hora=hora_sin_micro,
        total=total,
        tipo_pago=tipo_pago,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return RedirectResponse(
        url="/panel/ventas/nueva",
        status_code=303,
    )


# =========================
# Panel de Gastos
# =========================
@router.get("/panel/gastos", response_class=HTMLResponse)
def ver_gastos_web(
    request: Request,
    db: Session = Depends(get_db),
    fecha: date = Query(default_factory=date.today),
    current_user=Depends(get_current_active_user_from_cookie),
):
    gastos = (
        db.query(Gasto)
        .filter(Gasto.fecha == fecha)
        .order_by(Gasto.id.desc())
        .all()
    )

    total_dia = sum(g.monto for g in gastos) if gastos else 0

    return templates.TemplateResponse(
        "gastos.html",
        {
            "request": request,
            "gastos": gastos,
            "fecha": fecha,
            "total_dia": total_dia,
            "current_user": current_user,
        },
    )


# =========================
# Panel de Reportes
# =========================
@router.get("/panel/reportes", response_class=HTMLResponse)
def ver_reportes_web(
    request: Request,
    db: Session = Depends(get_db),
    fecha: date = Query(default_factory=date.today),
    rango: str = Query("dia"),  # dia | hoy | ayer | ultimos_7
    current_user=Depends(get_current_active_user_from_cookie),
):
    """
    Reporte diario / por rango:
    - Total de ventas
    - Total de gastos
    - Utilidad = total_ventas - total_gastos
    - Totales por tipo de pago
    - Detalle de ventas y gastos
    """

    rango = (rango or "dia").lower()

    # Determinar rango de fechas
    if rango == "hoy":
        fecha_ref = date.today()
        fecha_inicio = fecha_ref
        fecha_fin = fecha_ref
        rango_label = "Hoy"
    elif rango == "ayer":
        fecha_ref = date.today() - timedelta(days=1)
        fecha_inicio = fecha_ref
        fecha_fin = fecha_ref
        rango_label = "Ayer"
    elif rango == "ultimos_7":
        fecha_fin = date.today()
        fecha_inicio = fecha_fin - timedelta(days=6)
        rango_label = "Últimos 7 días"
    else:  # "dia" o cualquier otro valor
        fecha_ref = fecha
        fecha_inicio = fecha_ref
        fecha_fin = fecha_ref
        rango = "dia"
        rango_label = f"Día {fecha_ref.isoformat()}"

    # --- Ventas en el rango ---
    ventas = (
        db.query(Venta)
        .filter(Venta.fecha >= fecha_inicio, Venta.fecha <= fecha_fin)
        .order_by(Venta.fecha, Venta.hora)
        .all()
    )

    total_ventas = sum(v.total for v in ventas) if ventas else 0.0

    # Totales por tipo de pago
    totales_por_pago = defaultdict(float)
    for v in ventas:
        totales_por_pago[v.tipo_pago] += v.total

    # --- Gastos en el rango ---
    gastos = (
        db.query(Gasto)
        .filter(Gasto.fecha >= fecha_inicio, Gasto.fecha <= fecha_fin)
        .order_by(Gasto.fecha, Gasto.id)
        .all()
    )
    total_gastos = sum(g.monto for g in gastos) if gastos else 0.0

    # --- Utilidad ---
    utilidad = total_ventas - total_gastos

    # Para el input date usamos la fecha final (normalmente hoy)
    fecha_input = fecha_fin

    return templates.TemplateResponse(
        "reportes.html",
        {
            "request": request,
            "fecha": fecha_input,
            "rango": rango,
            "rango_label": rango_label,
            "ventas": ventas,
            "gastos": gastos,
            "total_ventas": total_ventas,
            "total_gastos": total_gastos,
            "utilidad": utilidad,
            "totales_por_pago": dict(totales_por_pago),
            "current_user": current_user,
        },
    )

