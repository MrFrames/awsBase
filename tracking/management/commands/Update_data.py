from django.core.management.base import BaseCommand, CommandError
from tracking.views import processData

class Command(BaseCommand):
    help = 'Updates data from spotgen & extrapolates existing data'

    def handle(self, *args, **options):
        processData(0, 0)
        processData(0, 24)
        print("new Data processed")