from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import EstudioLink
from django.utils.html import format_html


@admin.register(EstudioLink)
class EstudioLinkAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'estudio',
        'doctor',
        'vigencia',
        'link_display',
        'expired',
    )
    list_filter = ('doctor',)
    search_fields = ('estudio__study_uid', 'link')
    readonly_fields = ('vigencia', 'link_display')
    ordering = ('-vigencia',)

    def expired(self, obj):
        return obj.is_expired()
    expired.boolean = True
    expired.short_description = 'Expirado'

    def link_display(self, obj):
        # Muestra el link como enlace clicable
        return format_html('<a href="{}" target="_blank">{}</a>', obj.link, obj.link)
    link_display.short_description = 'Link'
