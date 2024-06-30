from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from django.core.cache import cache
from apps.dashboard.models import Location, Vendor, Account, Meter, RateSchedule, Service
from utils.data_parsers.csv_parser import parse_csv
from datetime import datetime
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate the database with initial data'
    BATCH_SIZE = 1000

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the uploaded CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        data = parse_csv(file_path)

        locations_cache = {}
        vendors_cache = {}
        accounts_cache = {}
        meters_cache = {}
        rate_schedules_cache = {}

        services_to_create = []

        record_count = 0
        cumulative_record_count = 0
        
        for record in data:
            location_name = record['Location Name']
            if location_name not in locations_cache:
                location, created = Location.objects.get_or_create(
                    name=location_name,
                    defaults={
                        'location_number': record['Location #'],
                        'total_bldg_sqft': record['Total Bldg SqFt'],
                    }
                )
                locations_cache[location_name] = location
            else:
                location = locations_cache[location_name]


            vendor_name = record['Vendor Name']
            if vendor_name not in vendors_cache:
                vendor, created = Vendor.objects.get_or_create(
                    name=vendor_name
                )
                vendor.locations.add(location)
                vendors_cache[vendor_name] = vendor
            else:
                vendor = vendors_cache[vendor_name]
                vendor.locations.add(location)


            account_number = record['Account #']
            if account_number not in accounts_cache:
                account, created = Account.objects.get_or_create(
                    account_number=account_number,
                    defaults={
                        'clean_account_number': record['Clean Account #'],
                        'supplier_only_account': record['Supplier Only Account'].lower() == 'true',
                        'audit_only': record['Audit Only'].lower() == 'yes',
                        'location': location
                    }
                )
                accounts_cache[account_number] = account
            else:
                account = accounts_cache[account_number]


            meter_number = record['Meter #']
            if meter_number:
                if meter_number not in meters_cache:
                    meter, created = Meter.objects.get_or_create(
                        meter_number=meter_number,
                        defaults={'location': location}
                    )
                    meters_cache[meter_number] = meter
                else:
                    meter = meters_cache[meter_number]
            else:
                meter = None


            rate_schedule_value = record['Rate Schedule']
            if rate_schedule_value:
                if rate_schedule_value not in rate_schedules_cache:
                    rate_schedule, created = RateSchedule.objects.get_or_create(
                        rate_schedule=rate_schedule_value
                    )
                    rate_schedule.locations.add(location)
                    rate_schedules_cache[rate_schedule_value] = rate_schedule
                else:
                    rate_schedule = rate_schedules_cache[rate_schedule_value]
                    rate_schedule.locations.add(location)
            else:
                rate_schedule = None


            valid_date = datetime.strptime(str(record['Month']), '%m/%d/%Y').date()

            service = Service(
                location=location,
                vendor=vendor,
                account=account,
                meter=meter,
                rate_schedule=rate_schedule,
                month=valid_date.month,
                year=valid_date.year,
                service_days=int(record['Service Days']),
                cost=Decimal(record['Cost']),
                service_type=record['Service Type'],
                uom=record['UOM'],
                usage=Decimal(record['Usage']),
                cost_per_unit=Decimal(record['Cost Per Unit']),
                kbtus=Decimal(record['KBTUs']),
                open_exceptions=record['Open Exceptions'].lower() == 'yes',
                bundle=record['Bundle'],
                entity=record['Entity']
            )
            # Ensure hash is calculated and set before saving
            service.hash = service.get_hash()

            if not Service.objects.filter(hash=service.hash).exists():
                services_to_create.append(service)
                record_count += 1
                cumulative_record_count += 1

                if record_count >= self.BATCH_SIZE:
                    try:
                        with transaction.atomic():
                            Service.objects.bulk_create(services_to_create, ignore_conflicts=False)
                        self.stdout.write(self.style.SUCCESS(f"{len(services_to_create)} records populated successfully"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error during bulk create: {str(e)}"))
                    services_to_create = []
                    record_count = 0

        # Insert any remaining records
        if services_to_create:
            try:
                with transaction.atomic():
                    Service.objects.bulk_create(services_to_create, ignore_conflicts=False)
                self.stdout.write(self.style.SUCCESS(f"{len(services_to_create)} records populated successfully"))
                cache.set('populate_data_message', f"{cumulative_record_count} records populated successfully!", timeout=60*15)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error during bulk create: {str(e)}"))
                cache.set('populate_data_message', f'Error populating data: {str(e)}', timeout=60*15)
        else:
            self.stdout.write(self.style.SUCCESS("No records to populate!"))
            cache.set('populate_data_message', 'No records to populate!', timeout=60*15)
