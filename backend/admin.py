from django.contrib import admin
from backend.models import Center, Sensor


@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Center._meta.fields]


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Sensor._meta.fields]
