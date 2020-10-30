from django.core.management.base import BaseCommand
from  covid_app.ReportMaker import initIndexPostUpdate
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        start =datetime.datetime.now()
        initIndexPostUpdate()
        print("Finished initIndexPostUpdate in " + str(datetime.datetime.now()- start))