from django_cron import CronJobBase, Schedule
from .views import processData, assign_sections

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 6
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'tracking.my_cron_job'
    
    def do(self):
        processData(0,0)
        processData(0,24)
        assign_sections(0)
        assign_sections(24)