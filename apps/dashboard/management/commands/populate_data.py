from django.core.management.base import BaseCommand
from django.db import transaction
from apps.dashboard.models import Location, Vendor, Account, Meter, RateSchedule, Service
from utils.data_parsers.csv_parser import process_folder
from datetime import datetime

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        data_folder_path = "/home/walmer/Projects/HighgateDashboard/.private/reports"
        data = process_folder(data_folder_path)

        count = 0
        for record in data:
            location, created = Location.objects.get_or_create(
                name=record['Location Name'],
                defaults={
                    'location_number': record['Location #'],
                    'total_bldg_sqft': record['Total Bldg SqFt'],
                }
            )

            vendor, created = Vendor.objects.get_or_create(
                name=record['Vendor Name']
            )
            vendor.locations.add(location)

            account, created = Account.objects.get_or_create(
                account_number=record['Account #'],
                defaults={
                    'clean_account_number': record['Clean Account #'],
                    'supplier_only_account': record['Supplier Only Account'].lower() == 'true',
                    'audit_only': record['Audit Only'].lower() == 'yes',
                    'location': location
                }
            )

            meter = None
            if record['Meter #']:
                meter, created = Meter.objects.get_or_create(
                    meter_number=record['Meter #'],
                    defaults={'location': location}
                )

            rate_schedule = None
            if record['Rate Schedule']:
                rate_schedule, created = RateSchedule.objects.get_or_create(
                    rate_schedule=record['Rate Schedule']
                )
                rate_schedule.locations.add(location)

            valid_date = datetime.strptime(str(record['Month']), '%m/%d/%Y').date()
            service, created = Service.objects.get_or_create(
                location=location,
                vendor=vendor,
                account=account,
                meter=meter,
                rate_schedule=rate_schedule,
                defaults={
                    'month': valid_date.month,
                    'year': valid_date.year,
                    'service_days': int(record['Service Days']),
                    'cost': float(record['Cost']),
                    'service_type': record['Service Type'],
                    'uom': record['UOM'],
                    'usage': float(record['Usage']),
                    'cost_per_unit': float(record['Cost Per Unit']),
                    'kbtus': float(record['KBTUs']),
                    'open_exceptions': record['Open Exceptions'].lower() == 'yes',
                    'bundle': record['Bundle'],
                    'entity': record['Entity']
                }
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} records populated successfully"))
