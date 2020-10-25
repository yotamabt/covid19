from django.core.management.base import BaseCommand
from  covid_app.utils import fullDataImportPCRTests
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        start =datetime.datetime.now()
        fullDataImportPCRTests()
        print("Finished fullDataImportPCRTests in " + str(datetime.datetime.now()- start))