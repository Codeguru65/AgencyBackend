from django.db import models

# Create your models here.
from authentication.models import User


class AgentSale(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    agent_category = models.CharField(max_length=255)
    agent_institution = models.CharField(max_length=255)
    agent_pricing = models.FloatField(default=0)
    product_name = models.CharField(max_length=255)
    vrn = models.CharField(max_length=10, blank=True)
    transaction_id = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=255)
    receipt_number = models.CharField(max_length=255)
    transaction_amount = models.FloatField(default=0)
    transaction_commission = models.FloatField(default=0)
    transaction_status = models.CharField(max_length=10, blank=True)
    transaction_date = models.DateTimeField(auto_now=True)
    commission_month = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    customer_email = models.CharField(max_length=255)
    customer_cell = models.CharField(max_length=255)
    customer_IDnumber = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Agent Sales'
        verbose_name_plural = 'Agent Sales'
