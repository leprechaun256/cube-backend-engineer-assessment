from __future__ import unicode_literals

from django.apps import AppConfig


class CubeAppConfig(AppConfig):
    name = 'cube'

    def ready(self):
        import cube.signals  # noqa: F401 imported but unused
