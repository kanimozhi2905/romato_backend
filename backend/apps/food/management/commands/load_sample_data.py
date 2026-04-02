from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Load sample data into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-input',
            action='store_true',
            help='Do not prompt for confirmation',
        )

    def handle(self, *args, **options):
        no_input = options['no_input']

        if not no_input:
            confirm = input(
                "This will delete all existing data and load sample data. Continue? (yes/no): "
            )
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING('Operation cancelled.'))
                return

        self.stdout.write(self.style.SUCCESS('Loading sample data...'))

        # Load categories and food items
        call_command('loaddata', 'sample_data.json')

        self.stdout.write(self.style.SUCCESS('\n✅ Sample data loaded successfully!'))
        self.stdout.write(self.style.SUCCESS('\nYou can now:'))
        self.stdout.write(self.style.SUCCESS('  1. Login to admin panel at http://127.0.0.1:8000/admin/'))
        self.stdout.write(self.style.SUCCESS('  2. Browse food items and categories'))
        self.stdout.write(self.style.SUCCESS('  3. Test the API endpoints'))
