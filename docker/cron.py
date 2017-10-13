import time

import schedule

import django
from django.core.management import call_command


def run_import():
    django.setup()
    call_command('import_data')

schedule.every(15).minutes.do(run_import)

while True:
    schedule.run_pending()
    time.sleep(1)
