from django.core.management.base import BaseCommand
from  covid_app.utils import TestsFullUpdateNoSymptoms
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        start =datetime.datetime.now()
        TestsFullUpdateNoSymptoms()
        print("Finished TestsFullUpdateNoSymptoms in " + str(datetime.datetime.now()- start ))