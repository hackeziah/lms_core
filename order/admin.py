from django.contrib import admin
from order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ('internalId', 'dateSampleTaken', )
    list_display = ('internalId', 'dateSampleTaken', 'status' )
    list_per_page = 20
    list_filter = ['status']
    search_fields = ['internalId', 'physician__firstName', 'physician__middleName', 
    'physician__lastName', 'hospital__name', 'hospital__address',]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(OrderAdmin, self).get_fields(request, obj)
        return (
            ('Order Details', {
                'fields': ('internalId', 'dateSampleTaken', 'sample', 
                'status', 'hospital', 'physician')
            }),
        )

admin.site.site_header = 'Mini Laboratory Management'