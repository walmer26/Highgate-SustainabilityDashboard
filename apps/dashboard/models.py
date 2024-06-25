from django.db import models
from utils.hashers.hash_record import hash_record
import uuid

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location_number = models.CharField(max_length=50)
    total_bldg_sqft = models.CharField(max_length=50, blank=True, null=True)

class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    locations = models.ManyToManyField(Location)

class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_number = models.CharField(max_length=50)
    clean_account_number = models.CharField(max_length=50)
    supplier_only_account = models.BooleanField()
    audit_only = models.BooleanField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

class Meter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meter_number = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

class RateSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rate_schedule = models.CharField(max_length=50)
    locations = models.ManyToManyField(Location)

class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, blank=True, null=True)
    rate_schedule = models.ForeignKey(RateSchedule, on_delete=models.CASCADE, blank=True, null=True)
    month = models.IntegerField()
    year = models.IntegerField()
    service_days = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_type = models.CharField(max_length=50)
    uom = models.CharField(max_length=50)
    usage = models.DecimalField(max_digits=10, decimal_places=3)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=3)
    kbtus = models.DecimalField(max_digits=10, decimal_places=3)
    open_exceptions = models.BooleanField()
    bundle = models.CharField(max_length=255)
    entity = models.CharField(max_length=255)
    hash = models.CharField(max_length=64, blank=True, editable=False)

    def get_hash(self):
        """
        Returns a hash of the specified fields of the service.
        """
        fields_to_hash = {
            'location_id': self.location.id,
            'vendor_id': self.vendor.id,
            'account_id': self.account.id,
            'meter_id': self.meter.id if self.meter else None,
            'rate_schedule_id': self.rate_schedule.id if self.rate_schedule else None,
            'month': self.month,
            'year': self.year,
            'service_days': self.service_days,
            'service_type': self.service_type,
        }
        return hash_record(**fields_to_hash)

    def save(self, *args, **kwargs):
        # Calculate the hash before saving
        self.hash = self.get_hash()
        super(Service, self).save(*args, **kwargs)
