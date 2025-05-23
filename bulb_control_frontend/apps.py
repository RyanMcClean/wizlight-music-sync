# pylint: disable=E1101
"""Django APP config, has init calls that only occur when bulb model table is present in database"""

from django.apps import AppConfig
from django.db import connections


class BulbControlFrontendConfig(AppConfig):
    """ "Django app config, used to initialize the app and set up the database connection"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "bulb_control_frontend"

    def ready(self):
        from . import variables  # pylint: disable=C0415
        from django.db import models  # pylint: disable=C0415, W0611

        if "bulb_control_frontend_wizbulb" in connections["default"].introspection.table_names():
            variables.init()
            variables.update_bulb_objects()
            variables.update_working_audio_devices()
