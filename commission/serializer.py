from rest_framework import serializers

from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from commission.models import AgentSale


class SalesSerializer(serializers.ModelSerializer):
    # default_error_messages = {
    #     'username': 'The username should only contain alphanumeric characters'}
    # agent_name= serializers.ReadOnlyField(source='agent.email')
    

    class Meta:
        model = AgentSale
        fields = ['id','agent_category','agent_institution','agent_pricing','product_name','vrn','transaction_id','policy_number','receipt_number','transaction_amount',
                  'transaction_commission','transaction_status','commission_month','customer_name', 'customer_email', 'customer_cell', 'customer_IDnumber']
