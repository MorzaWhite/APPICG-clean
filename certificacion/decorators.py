from functools import wraps
from django.db import OperationalError, transaction
import time
import logging

logger = logging.getLogger(__name__)

def retry_on_db_lock(retries=3, delay=0.2):
    """
    A decorator to retry a function when a database lock occurs.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    with transaction.atomic():
                        return func(*args, **kwargs)
                except OperationalError as e:
                    if 'database is locked' in str(e):
                        if i < retries - 1:
                            logger.warning(f"Database locked, retrying in {delay}s... ({i+1}/{retries})")
                            time.sleep(delay)
                        else:
                            logger.error(f"Database still locked after {retries} retries.")
                            raise e
                    else:
                        raise e
        return wrapper
    return decorator
