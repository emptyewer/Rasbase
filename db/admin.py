
from django.contrib import admin
from .models import Bait, Vector, IndexedGenome, PreyLibrary

class GeneModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(IndexedGenome, GeneModelAdmin)
admin.site.register(Bait, GeneModelAdmin)
admin.site.register(Vector, GeneModelAdmin)
admin.site.register(PreyLibrary, GeneModelAdmin)

