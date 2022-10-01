from django.contrib import admin

from systems_and_levels.models import System, Level


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )
