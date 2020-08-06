import os
__PATH_LOCALE = os.path.normpath(os.path.join(os.path.dirname(__file__), "../locale/"))

LANGUAGE_CODE = "es-MX"
LOCALE_PATHS = (__PATH_LOCALE, )

USE_I18N = True
USE_L10N = True
USE_TZ = True

gettext_noop = lambda s: s

PAGE_LANGUAGES = (
    ("es", gettext_noop("Español")),
    ("en", gettext_noop("Inglés")),
)

languages = list(PAGE_LANGUAGES)
LANGUAGES = languages


# Configuracion de formatos de fechas
DATETIME_INPUT_FORMATS = (
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%d-%m-%Y %H:%M:%S',     # '2006-10-25 14:30:59'
    '%d-%m-%Y %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%d-%m-%Y %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%d/%m/%Y %H:%M:%S',     # '31/12/2006 14:30:59'
    '%d/%m/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%d/%m/%Y %H:%M',        # '31/12/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
    '%m/%d/%y',              # '10/25/06'
    '%m/%d/%Y',              # '10/25/2006'
    '%d/%m/%Y',              # '10/25/2006'
    '%d/%m/%y',              # '10/25/06'
)

DATE_INPUT_FORMATS = (
    '%d/%m/%Y',                         # '10/25/2006'
    '%d/%m/%y',                         # '10/25/06'
)
