from django.contrib import admin
from .models import Club

class ClubAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'responsable') 
    search_fields = ('nombre',)
    
admin.site.register(Club, ClubAdmin)
