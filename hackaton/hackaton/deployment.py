import os
from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://'+os.environ['WEBSITE_HOSTNAME']]
DEBUG = True
SECRET_KEY = os.environ['MY_SECRET_KEY']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",

    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
raw = (
    os.getenv("CUSTOMCONNSTR_AZURE_POSTGRESQL_CONNECTIONSTRING")
    or os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING", "")
)

tokens = raw.replace(";", " ").split()
params = dict(t.split("=", 1) for t in tokens if "=" in t)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": params.get("dbname") or params.get("Database"),
        "USER": params.get("user") or params.get("User") or params.get("User Id"),
        "PASSWORD": params.get("password") or params.get("Password"),
        "HOST": params.get("host") or params.get("Server"),
        "PORT": params.get("port", "5432"),
        "OPTIONS": {"sslmode": params.get("sslmode", "require")},
    }
}
# connection_string = os.environ.get(
#     "CUSTOMCONNSTR_AZURE_POSTGRESQL_CONNECTIONSTRING", "")
#
# connection_params = {
#     param.split("=")[0].strip(): param.split("=")[1].strip()
#     for param in connection_string.split(";") if "=" in param
# }
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': connection_params.get('Database', 'default_db_name'),
#         'USER': connection_params.get('User Id', 'default_user'),
#         'PASSWORD': connection_params.get('Password', 'default_password'),
#         'HOST': connection_params.get('Server', 'localhost'),
#     }
# }


STATIC_ROOT = BASE_DIR/'staticfiles'
