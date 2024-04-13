import schedule
import time
from django.utils import timezone
from .models import Announcement


# aktivity klientu, smeny opatrovniku, oznameni na uvodni strance - 'nepernamentni veci'
# TODO: smazani tehle veci po prekroceni urciteho datumu a casu z database
# netusim jak udelat bez toho aby se musel pouzivat nejaky extra software pro periodicke volani fci nebo to fungovalo
# (celery, huey, background-tasks, chronograph [ten by snad mohl jit, ale pip ho nechce stahnout],
# schedule [tenhle soubor])


# fce na mazani oznameni z databaze potom po datu a case 'delete_on'
def check_announcement_delete_on():
    Announcement.objects.filter(
        delete_on__lte=timezone.now()
    ).delete()


schedule.every(10).hours.do(check_announcement_delete_on)

while True:
    schedule.run_pending()
    time.sleep(1)
