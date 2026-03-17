from wtforms import Form
from wtforms import StringField, IntegerField, DecimalField, DateField, SelectField
from wtforms import validators

class ClienteForm(Form):

    id_cliente = IntegerField('ID')

    nombre = StringField(
        'Nombre',
        [
            validators.DataRequired("El nombre es requerido"),
            validators.length(min=3, max=100)
        ]
    )

    direccion = StringField(
        'Dirección',
        [
            validators.DataRequired("La dirección es requerida"),
            validators.length(max=200)
        ]
    )

    telefono = StringField(
        'Teléfono',
        [
            validators.DataRequired("El teléfono es requerido"),
            validators.length(max=20)
        ]
    )
