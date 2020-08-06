#!/usr/bin/env python
import os
import sys
import re

def read_env_zappa():
    import json
    import os
    json_data = open('zappa_settings.json')
    env_vars = json.load(json_data)['dev']['environment_variables']
    for key, val in env_vars.items():
        os.environ[key] = val

def read_env_local():
    """Pulled from Honcho code with minor updates, reads local default
    environment variables from a .env file located in the project root
    directory.

    """
    try:
        with open('.env') as f:
            content = f.read()
    except IOError:
        content = ''

    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            os.environ.setdefault(key, val)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    # Settings var
    if 'SERVERTYPE' in os.environ and os.environ['SERVERTYPE'] == 'AWS Lambda':
        print('zappa loaded secret vars')
    else:
        read_env_local()

    execute_from_command_line(sys.argv)
