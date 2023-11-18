from django.contrib import admin
from . models import Reminder


class SearchAdmin(admin.ModelAdmin):
    """
    adding a panel to admin site for easy search
    """
    list_display = ['author', 'active', 'text', 'date']
    search_fields = ['author', 'date']
    list_filter = ['active', 'date', 'repeat', 'author']


admin.site.register(Reminder, SearchAdmin)
