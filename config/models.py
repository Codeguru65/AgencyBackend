from django.db import models
from authentication.models import User


categories = (
    ('CategoryA', 'CategoryA'),
    ('CategoryB', 'CategoryB'),
    ('CategoryC', 'CategoryC'),
    ('CategoryD', 'CategoryD'),
    ('CategoryE', 'CategoryE'),
    ('CategoryF', 'CategoryF'),
    ('CategoryG', 'CategoryG'),
)


class AgencyPricing(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=255, choices=categories)
    price = models.FloatField(default=0, help_text='Enter Percentage as Decimals')

    def __str__(self):
        return self.added_by.email


InsuranceUrlType = (
    ('ThirdPartyQoute', 'ThirdPartyQoute'),
    ('ThirdPartyPayment', 'ThirdPartyPayment'),
    ('ThirdPartyPolicy', 'ThirdPartyPolicy'),
    # Zinara Options
    ('ZinaraQuote', 'ZinaraQuote'),
    ('RadioQuote', 'RadioQuote'),
    ('LicensingPayment', 'LicensingPayment'),
    ('LicensingPolicy', 'LicensingPolicy'),
    # Combo
    ('ThirdPartyZinaraQoute', 'ThirdPartyZinaraQoute'),
    ('ThirdPartyZinaraPayment', 'ThirdPartyZinaraPayment'),
    ('ThirdPartyZinaraPolicy', 'ThirdPartyZinaraPolicy'),
    # Check Vehicle
    ('CheckVehicle', 'CheckVehicle')
)


class InsuranceApiUrlConfig(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)
    api_url = models.CharField(max_length=255)
    key_identifier = models.CharField(max_length=255, unique=True,
                                      choices=InsuranceUrlType,
                                      help_text='Select The Relevant Api Category Based On URL'
                                      )

    def __str__(self):
        return self.key_identifier

Endpoint_Name = (
    # Third Party
    ('3RDPARTYQUOTE', '3RDPARTYQUOTE'),
    ('3RDPARTYUPDATE', '3RDPARTYUPDATE'),
    ('3RDPARTYPOLICY', '3RDPARTYPOLICY'),

    # Comprehensive
    ('COMPREHENSIVEQUOTE', 'COMPREHENSIVEQUOTE'),

    # Reversal
    ('REVERSAL', 'REVERSAL'),
    # Licensing
    ('LICENSINGQUOTE', 'LICENSINGQUOTE'),
    ('LICENSINGUPDATE', 'LICENSINGUPDATE'),
    ('LICENSINGPOLICY', 'LICENSINGPOLICY'),

    # Combined
    ('COMBINEDQUOTE', 'COMBINEDQUOTE'),
    ('COMBINEDUPDATE', 'COMBINEDUPDATE'),
    ('COMBINEDPOLICY', 'COMBINEDPOLICY'),
)

# To assist the Admin to know the status of each added Endpoint
Env_Status = (
    ('LIVE', 'LIVE'),
    ('TEST', 'TEST')
)


class IceCashEndpoint(models.Model):
    api_name = models.CharField(choices=Endpoint_Name, max_length=255)
    api_endpoint = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    active_status = models.BooleanField(default=False)
    env_status = models.CharField(max_length=255, choices=Env_Status)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.api_endpoint


class InvoiceCount(models.Model):
    count = models.PositiveIntegerField(default=0)

    def __int__(self):
        return self.count


class ReceiptCount(models.Model):
    count = models.PositiveIntegerField(default=0)

    def __int__(self):
        return self.count


class PolicyScheduleCount(models.Model):
    count = models.PositiveIntegerField(default=0)

    def __int__(self):
        return self.count


# Prefix Tables
class InvoicePrefix(models.Model):
    prefix = models.CharField(max_length=255)

    def __str__(self):
        return self.prefix


class ReceiptPrefix(models.Model):
    prefix = models.CharField(max_length=255)

    def __str__(self):
        return self.prefix


class PolicySchedulePrefix(models.Model):
    prefix = models.CharField(max_length=255)

    def __str__(self):
        return self.prefix
