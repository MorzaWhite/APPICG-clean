# certificacion/business_hours.py

# Se importa ZoneInfo para el manejo moderno de zonas horarias, en lugar de pytz.
from zoneinfo import ZoneInfo
import datetime
from django.utils import timezone

# --- CONFIGURACIÓN DE HORARIO LABORAL ---
# Lunes a Viernes: 9:00 AM a 5:30 PM (17:30)
# Sábado: 9:00 AM a 1:00 PM (13:00)
# Domingo: No se trabaja.
BUSINESS_HOURS = {
    0: (datetime.time(9, 0), datetime.time(17, 30)),  # Lunes
    1: (datetime.time(9, 0), datetime.time(17, 30)),  # Martes
    2: (datetime.time(9, 0), datetime.time(17, 30)),  # Miércoles
    3: (datetime.time(9, 0), datetime.time(17, 30)),  # Jueves
    4: (datetime.time(9, 0), datetime.time(17, 30)),  # Viernes
    5: (datetime.time(9, 0), datetime.time(13, 0)),   # Sábado
    # El domingo (6) no se incluye, lo que significa que no es un día laboral.
}

# Se establece la zona horaria de Colombia. ZoneInfo es el estándar moderno de Python.
LOCAL_TZ = ZoneInfo('America/Bogota')

def _adjust_to_next_business_moment(dt):
    """
    Ajusta un datetime al inicio del próximo momento laboral disponible.
    Si el tiempo ya está en un momento laboral, lo devuelve sin cambios.

    Args:
        dt (datetime): La fecha y hora a ajustar.

    Returns:
        datetime: El próximo momento laboral válido.
    """
    # Se asegura de que el datetime esté en la zona horaria local para los cálculos.
    dt = dt.astimezone(LOCAL_TZ)

    # Bucle para asegurar que encontramos un día laboral.
    while dt.weekday() not in BUSINESS_HOURS:
        dt += datetime.timedelta(days=1)
        # Al pasar al siguiente día, reiniciamos la hora al inicio del día (00:00).
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    business_start, business_end = BUSINESS_HOURS[dt.weekday()]

    # Si es antes del horario laboral, se ajusta al inicio del día.
    if dt.time() < business_start:
        return dt.replace(hour=business_start.hour, minute=business_start.minute, second=0, microsecond=0)

    # Si es después del horario laboral, se mueve al inicio del día siguiente y se vuelve a ajustar.
    if dt.time() >= business_end:
        dt += datetime.timedelta(days=1)
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        # Llamada recursiva para manejar el nuevo día (que podría ser no laboral).
        return _adjust_to_next_business_moment(dt)

    # Si está dentro del horario laboral, se devuelve tal cual.
    return dt

def add_business_duration(start_time, duration_to_add):
    """
    Añade una duración a una fecha/hora de inicio, considerando solo el horario laboral.
    Esta función ha sido refactorizada para ser más clara y corregir errores de lógica.

    Args:
        start_time (datetime): Fecha y hora de inicio.
        duration_to_add (timedelta): Duración a añadir.

    Returns:
        datetime: La fecha y hora final, ajustada al horario laboral y en UTC.
    """
    # 1. Asegurar que el tiempo de inicio sea 'aware' (consciente de la zona horaria).
    if timezone.is_naive(start_time):
        # Se asume la zona horaria por defecto de Django si es 'naive'.
        start_time = timezone.make_aware(start_time, timezone.get_default_timezone())

    # 2. Convertir a la zona horaria local y ajustar al próximo momento laboral.
    current_time = _adjust_to_next_business_moment(start_time)

    remaining_seconds = duration_to_add.total_seconds()

    # 3. Bucle principal para añadir la duración.
    while remaining_seconds > 0:
        day_of_week = current_time.weekday()

        # Este 'if' es una salvaguarda, aunque _adjust_to_next_business_moment ya debería garantizarlo.
        if day_of_week in BUSINESS_HOURS:
            business_end_time = BUSINESS_HOURS[day_of_week][1]
            end_of_business_day = current_time.replace(
                hour=business_end_time.hour,
                minute=business_end_time.minute,
                second=0,
                microsecond=0
            )

            # Se calcula el tiempo disponible en el resto del día laboral.
            seconds_available_this_day = (end_of_business_day - current_time).total_seconds()

            # 4. Se añade el tiempo.
            if remaining_seconds <= seconds_available_this_day:
                # Si la duración restante cabe en el día actual, se añade y termina.
                current_time += datetime.timedelta(seconds=remaining_seconds)
                remaining_seconds = 0
            else:
                # Si no, se consume todo el tiempo disponible del día.
                remaining_seconds -= seconds_available_this_day
                # Se mueve al inicio del siguiente día para que la función de ajuste lo procese.
                next_day_start = current_time.date() + datetime.timedelta(days=1)
                current_time = _adjust_to_next_business_moment(
                    datetime.datetime.combine(next_day_start, datetime.time(0), tzinfo=LOCAL_TZ)
                )
        else:
            # Si por alguna razón caemos en un día no laboral, lo ajustamos.
            current_time = _adjust_to_next_business_moment(current_time)

    # 5. Se devuelve el resultado final en UTC para consistencia con la base de datos de Django.
    return current_time.astimezone(datetime.timezone.utc)

def subtract_business_duration(end_time, duration_to_subtract):
    """
    Resta una duración (timedelta) de una fecha/hora de finalización,
    considerando solo el horario laboral.
    """
    if timezone.is_naive(end_time):
        end_time = timezone.make_aware(end_time, timezone.get_default_timezone())

    current_time = end_time.astimezone(LOCAL_TZ)
    remaining_seconds = duration_to_subtract.total_seconds()

    while remaining_seconds > 0:
        day_of_week = current_time.weekday()

        if day_of_week in BUSINESS_HOURS:
            business_start, business_end = BUSINESS_HOURS[day_of_week]

            # Si la hora actual es después del fin de jornada, la ajustamos a ese fin.
            if current_time.time() > business_end:
                current_time = current_time.replace(hour=business_end.hour, minute=business_end.minute, second=0, microsecond=0)

            # Si es antes del inicio de jornada, saltamos al día anterior.
            if current_time.time() < business_start:
                current_time -= datetime.timedelta(days=1)
                # Nos movemos al final del día laboral anterior.
                prev_day_of_week = current_time.weekday()
                if prev_day_of_week in BUSINESS_HOURS:
                    _, prev_business_end = BUSINESS_HOURS[prev_day_of_week]
                    current_time = current_time.replace(hour=prev_business_end.hour, minute=prev_business_end.minute, second=0, microsecond=0)
                continue # Volvemos a evaluar el nuevo `current_time`.

            start_of_business_day = current_time.replace(hour=business_start.hour, minute=business_start.minute, second=0, microsecond=0)
            seconds_available_this_day = (current_time - start_of_business_day).total_seconds()

            if remaining_seconds <= seconds_available_this_day:
                current_time -= datetime.timedelta(seconds=remaining_seconds)
                remaining_seconds = 0
            else:
                remaining_seconds -= seconds_available_this_day
                current_time = start_of_business_day # Quedamos al inicio del día para seguir restando.
        else:
            # Si es un día no laboral, saltamos al día anterior.
            current_time -= datetime.timedelta(days=1)
            # Y nos posicionamos al final del horario laboral de ese día.
            prev_day_of_week = current_time.weekday()
            if prev_day_of_week in BUSINESS_HOURS:
                 _, prev_business_end = BUSINESS_HOURS[prev_day_of_week]
                 current_time = current_time.replace(hour=prev_business_end.hour, minute=prev_business_end.minute, second=0, microsecond=0)

    return current_time.astimezone(datetime.timezone.utc)
