from django.apps import AppConfig


class DoctorsConfig(AppConfig):
    name = 'Doctors'
    verbose_name = "پزشکان"

    def ready(self):
        import Doctors.signals
