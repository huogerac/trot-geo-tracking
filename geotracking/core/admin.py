from django.contrib import admin

from .models import Track


class TrackAdmin(admin.ModelAdmin):
    list_display = ("description", "done")


admin.site.register(Track, TrackAdmin)
