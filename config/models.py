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