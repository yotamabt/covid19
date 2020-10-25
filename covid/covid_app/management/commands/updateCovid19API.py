from django.core.management.base import BaseCommand
from  covid_app.utils import covid19APIUpdate
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        start =datetime.datetime.now()
        covid19APIUpdate()
        print("Finished covid19APIUpdate in " + str(datetime.datetime.now()- start))