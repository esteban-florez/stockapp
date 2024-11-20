from django.core.management.base import BaseCommand
from stock.seeder import seed

class Command(BaseCommand):
  help = "Seeds the database with test data"

  def handle(self, *args, **options):
    seed()

    self.stdout.write(
        self.style.SUCCESS('Database successfully seeded.')
    )
