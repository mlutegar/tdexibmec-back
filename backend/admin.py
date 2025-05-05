from django.contrib import admin

from backend.models import Palestrante, Pontuacao, Espectador


class PalestranteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')


class EspectadorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'avatar')
    list_filter = ('nome',)
    search_fields = ('nome',)


admin.site.register(Palestrante, PalestranteAdmin)
admin.site.register(Espectador, EspectadorAdmin)
admin.site.register(Pontuacao)
