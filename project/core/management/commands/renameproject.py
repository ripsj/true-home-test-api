import os
from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    help = 'Renames a Django project'

    def add_arguments(self, parser):
        parser.add_argument('new_project_name', type=str, help='The new Django project name')

    def handle(self, *args, **kwargs):
        new_project_name = kwargs['new_project_name']

        # Logica para renombrar los archivos
        files_to_rename = ['project/settings.py', 'project/wsgi.py', 'manage.py']
        folder_to_rename = 'project'

        for f in files_to_rename:
            with open(f, 'r') as file:
                filedata = file.read()

                # Cada que se renombra un proyecto se genera una nueva secret key
                if file.name == 'project/settings.py':
                    new_key = get_random_secret_key()
                    filedata = filedata.replace('hm_z3y!2-528ui5@ozg(c$_w82uj(4b_-yp4e!wmos1c+a869^', new_key)

            filedata = filedata.replace('project', new_project_name)

            with open(f, 'w') as file:
                file.write(filedata)

        os.rename(folder_to_rename, new_project_name)
        os.makedirs(f'{new_project_name}/media')

        self.stdout.write(self.style.SUCCESS(f'Project has been renamed to {new_project_name}'))
