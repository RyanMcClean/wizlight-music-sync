from django.apps import AppConfig
from django.db import connections


class BulbcontrolfrontendConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bulbControlFrontend"

    def ready(self):
        import bulbControlFrontend.variables as variables
        from django.db import models

        if "bulbControlFrontend_wizbulb" in connections["default"].introspection.table_names():
            variables.init()
            variables.update_bulb_objects()
            variables.update_working_audio_devices()
