from django.core.management.base import BaseCommand
from  covid_app.utils import agg
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        start =datetime.datetime.now()
        agg()
        print("Finished agg in " + str(datetime.datetime.now()- start))