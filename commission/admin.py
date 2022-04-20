from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(AgentSale)
class TransactionAdmin(admin.ModelAdmin):

    exclude = ['agent']
    list_display = ['agent', 'agent_category', 'agent_institution', 'agent_pricing','product_name','vrn','commission_month']

