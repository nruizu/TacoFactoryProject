#Autor: Samuel Gutierrez

from django.test import TestCase
from django.contrib.auth import get_user_model
from menu.models import Plato, Bebida
from carrito.models import Carrito, CarritoPlato, CarritoBebida

User = get_user_model()

class PruebasSimples(TestCase):

    def setUp(self):
        # Crear usuario para asociar al carrito
        self.usuario = User.objects.create_user(username='cliente', password='clave123')
        self.carrito = Carrito.objects.create(usuario=self.usuario)

        # Crear un plato y bebida de ejemplo
        self.plato = Plato.objects.create(
            idPlato='p1',
            nombre='Taco al pastor',
            descripcion='Taco con carne al pastor',
            precio=12.5,
            categoria='Plato Fuerte'
        )

        self.bebida = Bebida.objects.create(
            idBebida='b1',
            nombre='Coca Cola',
            descripcion='Bebida gaseosa',
            precio=3.0,
            categoria='Gaseosa',
            cantidad='280 ml'
        )

    def test_creacion_plato(self):
        self.assertEqual(self.plato.nombre, 'Taco al pastor')
        self.assertEqual(self.plato.precio, 12.5)
        self.assertEqual(self.plato.categoria, 'Plato Fuerte')

    def test_calculo_subtotal_carrito(self):
        # Agregar elementos al carrito
        CarritoPlato.objects.create(carrito=self.carrito, plato=self.plato, cantidad=2)  # 12.5 * 2 = 25
        CarritoBebida.objects.create(carrito=self.carrito, bebida=self.bebida, cantidad=3)  # 3.0 * 3 = 9

        subtotal = self.carrito.calcular_subtotal()
        self.assertEqual(subtotal, 34.0)
