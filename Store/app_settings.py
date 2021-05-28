from .models import CanteenSettings

class Settings:
    @staticmethod
    def app_settings():
        settings = CanteenSettings.objects.get(name='canteen')
        return settings
