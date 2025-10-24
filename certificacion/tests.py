from django.test import TestCase
from django.utils import timezone
import datetime
from .models import ConfiguracionTiempos
from .business_hours import add_business_duration

class BusinessHoursTests(TestCase):
    def setUp(self):
        # Configurar tiempos para los tipos de item que se usarán en las pruebas
        ConfiguracionTiempos.objects.create(
            tipo_item='JOYA',
            tipo_certificado='GC_SENCILLA',
            tiempo_ingreso=3600,  # 1 hora
            tiempo_fotografia=7200,  # 2 horas
            tiempo_revision=10800,  # 3 horas
            tiempo_impresion=1800,  # 0.5 horas
        )
        ConfiguracionTiempos.objects.create(
            tipo_item='PIEDRA',
            tipo_certificado='GC_SENCILLA',
            tiempo_ingreso=1800,
            tiempo_fotografia=3600,
            tiempo_revision=5400,
            tiempo_impresion=900
        )

    def test_add_business_duration_within_day(self):
        """Prueba que la duración se añade correctamente dentro de un mismo día laboral."""
        start_time = timezone.make_aware(datetime.datetime(2025, 10, 13, 10, 0, 0))  # Lunes a las 10:00
        duration = datetime.timedelta(hours=2)
        expected_end_time = timezone.make_aware(datetime.datetime(2025, 10, 13, 12, 0, 0))

        # Convertir a UTC para la comparación, ya que la función devuelve UTC
        result_utc = add_business_duration(start_time, duration)
        expected_utc = expected_end_time.astimezone(datetime.timezone.utc)

        self.assertAlmostEqual(result_utc, expected_utc, delta=datetime.timedelta(seconds=1))

    def test_add_business_duration_overnight(self):
        """Prueba que la duración se calcula correctamente pasando al día siguiente."""
        # Lunes a las 17:00, añadir 3 horas. Debería terminar el Martes a las 11:30
        # 0.5 horas el lunes (de 17:00 a 17:30)
        # 2.5 horas el martes (de 9:00 a 11:30)
        start_time = timezone.make_aware(datetime.datetime(2025, 10, 13, 17, 0, 0))
        duration = datetime.timedelta(hours=3)
        expected_end_time = timezone.make_aware(datetime.datetime(2025, 10, 14, 11, 30, 0))

        result_utc = add_business_duration(start_time, duration)
        expected_utc = expected_end_time.astimezone(datetime.timezone.utc)

        self.assertAlmostEqual(result_utc, expected_utc, delta=datetime.timedelta(seconds=1))

    def test_add_business_duration_over_weekend(self):
        """Prueba el cálculo de duración que atraviesa un fin de semana."""
        # Viernes a las 17:00, añadir 5 horas.
        # 0.5 horas el viernes (17:00 - 17:30)
        # 4 horas el sábado (9:00 - 13:00)
        # 0.5 horas el lunes (9:00 - 9:30)
        # El resultado esperado es el Lunes 13 de Octubre a las 9:30
        start_time = timezone.make_aware(datetime.datetime(2025, 10, 10, 17, 0, 0)) # Viernes
        duration = datetime.timedelta(hours=5)
        expected_end_time = timezone.make_aware(datetime.datetime(2025, 10, 13, 9, 30, 0))

        result_utc = add_business_duration(start_time, duration)
        expected_utc = expected_end_time.astimezone(datetime.timezone.utc)

        self.assertAlmostEqual(result_utc, expected_utc, delta=datetime.timedelta(seconds=1))

    def test_start_time_outside_business_hours(self):
        """Prueba que si se empieza fuera de horario, el cálculo inicia en el siguiente horario laboral."""
        # Empezar un domingo. El cálculo debería empezar el lunes a las 9:00.
        start_time = timezone.make_aware(datetime.datetime(2025, 10, 12, 14, 0, 0)) # Domingo
        duration = datetime.timedelta(hours=2)
        expected_end_time = timezone.make_aware(datetime.datetime(2025, 10, 13, 11, 0, 0)) # Lunes a las 11:00

        result_utc = add_business_duration(start_time, duration)
        expected_utc = expected_end_time.astimezone(datetime.timezone.utc)

        self.assertAlmostEqual(result_utc, expected_utc, delta=datetime.timedelta(seconds=1))

    def test_sequential_calculation(self):
        """Prueba el cálculo secuencial de dos items."""
        # Item 1: Empieza el lunes a las 16:00, dura 3 horas.
        # 1.5 horas el lunes (16:00 a 17:30)
        # 1.5 horas el martes (9:00 a 10:30)
        # Fecha límite item 1: Martes a las 10:30
        start_time_item1 = timezone.make_aware(datetime.datetime(2025, 10, 13, 16, 0, 0))
        duration_item1 = datetime.timedelta(hours=3)
        deadline_item1 = add_business_duration(start_time_item1, duration_item1)

        # Item 2: Empieza donde termina el item 1 (Martes 10:30), dura 4 horas.
        # Termina el Martes a las 14:30
        duration_item2 = datetime.timedelta(hours=4)
        expected_final_deadline = timezone.make_aware(datetime.datetime(2025, 10, 14, 14, 30, 0))

        # El punto de partida del item 2 es la fecha límite del item 1
        final_deadline = add_business_duration(deadline_item1, duration_item2)

        expected_utc = expected_final_deadline.astimezone(datetime.timezone.utc)

        self.assertAlmostEqual(final_deadline, expected_utc, delta=datetime.timedelta(seconds=1))

# from django.urls import reverse
# from .models import Orden, Item
# from django.contrib.auth.models import User

# class SetManualDateTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='password')
#         self.client.login(username='testuser', password='password')
#         self.orden = Orden.objects.create(numero_orden_facturacion='ORD-MANUAL-DATE-001')
#         self.item = Item.objects.create(orden=self.orden, numero_item=1, gema_principal='Diamante')

#     def test_set_manual_date(self):
#         """Prueba que se puede establecer la fecha de entrega manual."""
#         url = reverse('set_manual_date', args=[self.orden.id])
#         manual_date = timezone.localtime(timezone.now() + datetime.timedelta(days=5))

#         response = self.client.post(url, {
#             'fecha_entrega_manual': manual_date.strftime('%Y-%m-%dT%H:%M')
#         })

#         # Verificar que se redirige al dashboard
#         self.assertRedirects(response, reverse('dashboard'))

#         # Verificar que la fecha se guardó correctamente en el último item
#         self.item.refresh_from_db()
#         self.assertAlmostEqual(self.item.fecha_limite_etapa, manual_date, delta=datetime.timedelta(minutes=1))