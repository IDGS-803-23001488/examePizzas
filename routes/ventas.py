from flask import Flask, render_template, Blueprint, request, redirect, url_for, session
from forms import ClienteForm 
from models import db, Clientes, Pedidos, Pizzas, DetallePedido
import datetime

ventas = Blueprint(
    'ventas',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/ventas'
)

@ventas.route("/", methods=['GET','POST'])
def index():
    client_form = ClienteForm(request.form)
    now = datetime.datetime.now()
    
    if 'cliente' in session and request.method == "GET":
        cliente_data = session['cliente']
        client_form.nombre.data = cliente_data.get('nombre', '')
        client_form.direccion.data = cliente_data.get('direccion', '')
        client_form.telefono.data = cliente_data.get('telefono', '')

    if 'carrito' not in session:
        session['carrito'] = []

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "agregar_pizza":
            if not client_form.nombre.data or not client_form.direccion.data or not client_form.telefono.data:
                return redirect(url_for('ventas.index'))
            
            session['cliente'] = {
                "nombre": client_form.nombre.data,
                "direccion": client_form.direccion.data,
                "telefono": client_form.telefono.data
            }
            return redirect(url_for('ventas.agregar_pizza'))

        if accion == "finalizar":
            dia = request.form.get("dia")
            mes = request.form.get("mes")
            anio = request.form.get("anio")
            
            if not dia or not mes or not anio:
                return redirect(url_for('ventas.index'))
            
            fecha_pedido = datetime.date(int(anio), int(mes), int(dia))
            
            cliente_data = session.get('cliente')
            carrito = session.get('carrito')
            
            if not cliente_data or not carrito:
                return redirect(url_for('ventas.index'))

            try:
                cliente = Clientes(**cliente_data)
                db.session.add(cliente)
                db.session.flush()

                pedido = Pedidos(
                    id_cliente=cliente.id_cliente,
                    fecha=fecha_pedido,
                    total=0
                )

                db.session.add(pedido)
                db.session.flush()

                total = 0

                for item in carrito:
                    ingredientes_str = ', '.join(item['ingredientes']) if isinstance(item['ingredientes'], list) else item['ingredientes']
                    
                    pizza = Pizzas(
                        tamano=item['tamano'],
                        ingredientes=ingredientes_str,
                        precio=float(item['precio'])
                    )

                    db.session.add(pizza)
                    db.session.flush()

                    subtotal = float(item['precio']) * int(item['cantidad'])
                    total += subtotal

                    detalle = DetallePedido(
                        id_pedido=pedido.id_pedido,
                        id_pizza=pizza.id_pizza,
                        cantidad=item['cantidad'],
                        subtotal=subtotal
                    )

                    db.session.add(detalle)

                pedido.total = total
                db.session.commit()
                
                session.clear()
                
                return redirect(url_for('ventas.index'))
                
            except Exception as e:
                db.session.rollback()
                print(f"Error al guardar el pedido: {e}")
                return redirect(url_for('ventas.index'))

        if accion == "eliminar_pizza":
            index = request.form.get("index")
            if index is not None and 'carrito' in session:
                try:
                    index = int(index)
                    if 0 <= index < len(session['carrito']):
                        session['carrito'].pop(index)
                        session.modified = True
                except (ValueError, IndexError):
                    pass
            return redirect(url_for('ventas.index'))

    return render_template(
        "ventas/pdv.html",
        client_form=client_form,
        carrito=session.get('carrito', []),
        now=now
    )

@ventas.route("/pizza", methods=['GET','POST'])
def agregar_pizza():
    if request.method == "POST":
        tamano = request.form.get("tamano")
        ingredientes = request.form.getlist("ingredientes")
        cantidad = int(request.form.get("cantidad"))

        precios = {
            "chica": 40,
            "mediana": 80,
            "grande": 120
        }

        precio_base = precios.get(tamano, 40)
        precio_ingredientes = len(ingredientes) * 10
        precio_total = precio_base + precio_ingredientes

        pizza = {
            "tamano": tamano,
            "ingredientes": ingredientes,
            "cantidad": cantidad,
            "precio": precio_total
        }

        carrito = session.get("carrito", [])
        carrito.append(pizza)
        session["carrito"] = carrito

        return redirect(url_for("ventas.index"))

    return render_template("ventas/pizza.html")
