from django.core.management.base import BaseCommand
from apps.dashboard.tasks import populate_data

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the uploaded CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        populate_data(file_path)  # Trigger background task
        self.stdout.write(self.style.SUCCESS('Data population started in the background.'))
