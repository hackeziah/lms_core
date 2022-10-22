from django.contrib import admin
from hospital.models import Physician, Patient, Sample,\
     Hospital, LaboratoryStorage


@admin.register(Physician)
class PhysicianAdmin(admin.ModelAdmin):
    ordering = ('created',)
    list_display = ('full_name', 'created', 'lastUpdated')
    list_per_page = 20
    search_fields = ['firstName', 'middleName', 'lastName', 'address', 'phoneNumber',]
    read_only = ('created', 'lastUpdated')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(PhysicianAdmin, self).get_fields(request, obj)
        return (
            ('Physician Details', {
                'fields': ('firstName', 'middleName', 'lastName', 'address', 'phoneNumber',)
            }),
        )



@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    ordering = ('created',)
    list_display = ('full_name', 'created','lastUpdated')
    list_per_page = 20
    search_fields = ['firstName', 'middleName', 'lastName', 'address', 'phoneNumber',]
    read_only = ('created', 'full_name', 'lastUpdated')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(PatientAdmin, self).get_fields(request, obj)
        return (
            ('Patient Details', {
                'fields': ('firstName', 'middleName', 'lastName', 'address', 'phoneNumber',)
            }),
        )



@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    ordering = ('sampleId', 'created',)
    list_display = ('sampleId', 'created',)
    list_per_page = 20
    search_fields = ['sampleId', 'patient__firstName', 'patient__middleName', 'patient__lastName',]
    read_only = ('created')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(SampleAdmin, self).get_fields(request, obj)
        return (
            ('Sample Details', {
                'fields': ('sampleId', 'patient', )
            }),
        )

    
@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    ordering = ('name', 'created',)
    list_display = ('name', 'created',)
    list_per_page = 20
    search_fields = ('name', 'address',)
    read_only = ('created')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(HospitalAdmin, self).get_fields(request, obj)
        return (
            ('Hospital Details', {
                'fields': ('name', 'address', )
            }),
        )


@admin.register(LaboratoryStorage)
class LaboratoryStorageAdmin(admin.ModelAdmin):
    ordering = ('name', 'created',)
    list_display = ('name', 'created',)
    list_per_page = 20
    search_fields = ('name', 'location',)
    read_only = ('created',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(LaboratoryStorageAdmin, self).get_fields(request, obj)
        return (
            ('Laboratory Storage Details', {
                'fields': ('name', 'location', 'orders')
            }),
        )

