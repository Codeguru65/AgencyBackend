from datetime import datetime
import requests
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from authentication.models import User
from commission.models import AgentSale
from commission.serializer import SalesSerializer
from config.models import AgencyPricing
from apirequests.apiurls import ThirdPartyQoute, CheckVehicle, ThirdPartyPayment, ThirdPartyPolicy
from config.models import InsuranceApiUrlConfig


# Agent Sales
# @api_view(['GET', 'POST'])
class CommissionsView(views.APIView):
    period_param_config = openapi.Parameter('period', in_=openapi.IN_QUERY, description='Month and Year',
                                            type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[period_param_config, ])
    def get(self, request):
        period = request.GET.get('period')
        if request.user.is_manager:
            snippets = AgentSale.objects.filter(agent_institution=request.user.institution.name,
                                                commission_month=period)
            all_sum = snippets.aggregate(Sum('transaction_commission'))
            print(all_sum)
            serializer = SalesSerializer(snippets, many=True)
            if serializer:
                return JsonResponse(serializer.data, safe=False)
            else:
                response = {"message": "No Records To Show"}
                return JsonResponse(response, safe=False)
        else:
            print(request.user, period, 'im the user')
            snippets = AgentSale.objects.filter(agent=request.user,
                                                commission_month=period)
            serializer = SalesSerializer(snippets, many=True)
            print('im here', snippets)
            if serializer:
                return JsonResponse(serializer.data, safe=False)
            else:
                response = {"message": "No Records To Show"}
                return JsonResponse(response, safe=False)


class CommissionsSummedView(views.APIView):
    period_param_config = openapi.Parameter('period', in_=openapi.IN_QUERY, description='Month and Year',
                                            type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[period_param_config, ])
    def get(self, request):
        period = request.GET.get('period')
        if request.user.is_manager:
            snippets = AgentSale.objects.filter(agent_institution=request.user.institution.name,
                                                commission_month=period)
            rta_count = AgentSale.objects.filter(agent_institution=request.user.institution.name,
                                                 commission_month=period,
                                                 product_name='Third Party Insurance (RTA)').count()
            combo_count = AgentSale.objects.filter(agent_institution=request.user.institution.name,
                                                   commission_month=period,
                                                   product_name='Third Party Insurance (RTA) -Less Zinara').count()
            zinara_count = AgentSale.objects.filter(agent_institution=request.user.institution.name,
                                                    commission_month=period,
                                                    product_name='Zinara Only').count()
            all_sum = snippets.aggregate(Sum('transaction_commission'))
            print(rta_count)
            print(all_sum)
            serializer = SalesSerializer(snippets, many=True)
            if serializer:
                return JsonResponse(
                    {'commission_earned': all_sum, 'rta_count': rta_count, 'insurance_zinara_count': combo_count,
                     'zinara_count': zinara_count})
            else:
                response = {"message": "No Records To Show"}
                return JsonResponse(response, safe=False)
        else:
            print(request.user, period, 'im the user')
            snippets = AgentSale.objects.filter(agent=request.user,
                                                commission_month=period)
            rta_count = AgentSale.objects.filter(agent=request.user,
                                                 commission_month=period,
                                                 product_name='Third Party Insurance (RTA)').count()
            combo_count = AgentSale.objects.filter(agent=request.user,
                                                   commission_month=period,
                                                   product_name='Third Party Insurance (RTA) -Less Zinara').count()

            zinara_count = AgentSale.objects.filter(agent=request.user,
                                                    commission_month=period,
                                                    product_name='Zinara Only').count()
            all_sum = snippets.aggregate(Sum('transaction_commission'))
            print(rta_count)
            serializer = SalesSerializer(snippets, many=True)
            print('im here', snippets)
            if serializer:
                return JsonResponse(
                    {'commission_earned': all_sum, 'rta': rta_count, 'insurance_zinara_count': combo_count,
                     'zinara_count': zinara_count})
            else:
                response = {"message": "No Records To Show"}
                return JsonResponse(response, safe=False)
