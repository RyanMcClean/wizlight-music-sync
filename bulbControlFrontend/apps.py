from django.apps import AppConfig


class BulbcontrolfrontendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bulbControlFrontend'
    def ready(self):
        import bulbControlFrontend.variables
        bulbControlFrontend.variables.init()
        bulbControlFrontend.variables.update_bulb_objects()
        bulbControlFrontend.variables.update_working_audio_devices()

