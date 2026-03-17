from flask import Blueprint, render_template, request
from models import db, Pedidos, DetallePedido, Clientes, Pizzas
import datetime
from sqlalchemy import func

consultas = Blueprint(
    'consultas',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/consultas'
)


@consultas.route("/", methods=['GET'])
def index():

    now = datetime.datetime.now()
    fecha_actual = now.date()

    # Obtener pedidos del día
    pedidos_dia = db.session.query(Pedidos).filter(
        func.date(Pedidos.fecha) == fecha_actual
    ).all()

    total_pedidos = len(pedidos_dia)
    total_ventas = sum(pedido.total for pedido in pedidos_dia)

    resultados = []

    for pedido in pedidos_dia:

        cliente = Clientes.query.get(pedido.id_cliente)

        detalles = DetallePedido.query.filter_by(
            id_pedido=pedido.id_pedido
        ).all()

        pizzas_detalle = []

        for detalle in detalles:

            pizza = Pizzas.query.get(detalle.id_pizza)

            pizzas_detalle.append({
                "tamano": pizza.tamano,
                "ingredientes": pizza.ingredientes,
                "cantidad": detalle.cantidad,
                "precio_unitario": pizza.precio,
                "subtotal": detalle.subtotal
            })

        resultados.append({
            "id_pedido": pedido.id_pedido,
            "cliente": cliente.nombre if cliente else "Cliente no encontrado",
            "fecha": pedido.fecha.strftime('%d/%m/%Y'),
            "total": pedido.total,
            "pizzas": pizzas_detalle
        })

    # Estadísticas
    estadisticas = {
        "total_pizzas_vendidas": sum(
            sum(p["cantidad"] for p in pedido["pizzas"])
            for pedido in resultados
        ),
        "pedido_mas_alto": max(
            (pedido["total"] for pedido in resultados),
            default=0
        ),
        "pedido_mas_bajo": min(
            (pedido["total"] for pedido in resultados),
            default=0
        ),
        "promedio_por_pedido": (
            total_ventas / total_pedidos if total_pedidos > 0 else 0
        )
    }

    return render_template(
        "consultas/ventas_dia.html",
        now=now,
        fecha_actual=fecha_actual.strftime('%d/%m/%Y'),
        resultados=resultados,
        total_ventas=total_ventas,
        total_pedidos=total_pedidos,
        estadisticas=estadisticas
    )


@consultas.route("/historico", methods=['GET'])
def historico():

    tipo = request.args.get("tipo")
    valor = request.args.get("valor")

    # MySQL DAYOFWEEK: domingo=1 ... sábado=7
    dias_semana = {
        "domingo":1,
        "lunes":2,
        "martes":3,
        "miercoles":4,
        "jueves":5,
        "viernes":6,
        "sabado":7
    }

    meses = {
        "enero":1,
        "febrero":2,
        "marzo":3,
        "abril":4,
        "mayo":5,
        "junio":6,
        "julio":7,
        "agosto":8,
        "septiembre":9,
        "octubre":10,
        "noviembre":11,
        "diciembre":12
    }

    query = db.session.query(Pedidos)

    if tipo == "dia":
        numero_dia = dias_semana.get(valor.lower())
        query = query.filter(
            func.dayofweek(Pedidos.fecha) == numero_dia
        )

    elif tipo == "mes":
        numero_mes = meses.get(valor.lower())
        query = query.filter(
            func.month(Pedidos.fecha) == numero_mes
        )

    pedidos = query.all()

    total_pedidos = len(pedidos)
    total_ventas = sum(p.total for p in pedidos)

    resultados = []

    for pedido in pedidos:
        cliente = Clientes.query.get(pedido.id_cliente)
        detalles = DetallePedido.query.filter_by(
            id_pedido=pedido.id_pedido
        ).all()
        pizzas_detalle = []
        for detalle in detalles:
            pizza = Pizzas.query.get(detalle.id_pizza)
            pizzas_detalle.append({
                "tamano": pizza.tamano,
                "ingredientes": pizza.ingredientes,
                "cantidad": detalle.cantidad,
                "precio_unitario": pizza.precio,
                "subtotal": detalle.subtotal
            })
        resultados.append({
            "id_pedido": pedido.id_pedido,
            "cliente": cliente.nombre if cliente else "Cliente no encontrado",
            "fecha": pedido.fecha.strftime('%d/%m/%Y'),
            "total": pedido.total,
            "pizzas": pizzas_detalle
        })

    return render_template(
        "consultas/ventas_historico.html",
        resultados=resultados,
        total_ventas=total_ventas,
        total_pedidos=total_pedidos,
        filtro=f"{tipo} {valor}",
        tipo=tipo,
        valor=valor
    )


@consultas.route("/detalle/<int:id_pedido>", methods=['GET'])
def detalle(id_pedido):

    pedido = Pedidos.query.get_or_404(id_pedido)

    cliente = Clientes.query.get(pedido.id_cliente)

    detalles = DetallePedido.query.filter_by(
        id_pedido=id_pedido
    ).all()

    pizzas = []

    for detalle in detalles:

        pizza = Pizzas.query.get(detalle.id_pizza)

        pizzas.append({
            "tamano": pizza.tamano,
            "ingredientes": pizza.ingredientes,
            "cantidad": detalle.cantidad,
            "precio": pizza.precio,
            "subtotal": detalle.subtotal
        })

    return render_template(
        "consultas/detalle_pedido.html",
        pedido=pedido,
        cliente=cliente,
        pizzas=pizzas
    )