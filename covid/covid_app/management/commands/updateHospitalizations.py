from django.core.management.base import BaseCommand
from  covid_app.utils import hospitalizationUpdate
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        start =datetime.datetime.now()
        hospitalizationUpdate()
        print("Finished hospitalizationUpdate in " + str(datetime.datetime.now()- start))