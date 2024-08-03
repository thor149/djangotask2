from django.apps import AppConfig

class AppointmentSchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointmentScheduler'

    def ready(self):
        import appointmentScheduler.signals
