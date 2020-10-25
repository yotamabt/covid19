from django.core.management.base import BaseCommand
from  covid_app.utils import deathsNoDateUpdate
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        start =datetime.datetime.now()
        TestsFullUpdateNoSymptoms()
        print("Finished deathsNoDateUpdate in " + str(datetime.datetime.now()- start ))