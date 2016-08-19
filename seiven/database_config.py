# coding=utf-8
DATABASES_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<DB_NAME>',
        'USER': '<DB_USER>',
        'PASSWORD': '<DB_PASSWORD>',
        'HOST': '<DB_SERVER>',
        'PORT': '<DB_SERVER_PORT>',
        'ATOMIC_REQUESTS': True, # Crea transacciones en cada peticion de la vista
    }
}