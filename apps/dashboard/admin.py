from django.contrib import admin
from .models import Location, Vendor, Account, Meter, RateSchedule, Service


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'location_number',
        'total_bldg_sqft',
    ]

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        'account_number',
        'clean_account_number',
        'supplier_only_account',
        'audit_only',
        'location',
    ]

@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = [
        'meter_number',
        'location',
    ]

@admin.register(RateSchedule)
class RateScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'rate_schedule',
    ]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'location',
        'vendor',
        'account',
        'meter',
        'rate_schedule',
        'month',
        'year',
        'service_days',
        'cost',
        'service_type',
        'uom',
        'usage',
        'cost_per_unit',
        'kbtus',
        'open_exceptions',
        'bundle',
        'entity',
        'hash',
    ]

