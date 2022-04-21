from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import requests
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from authentication.models import User

# imports from yako
from apirequests.apiurls import ThirdPartyQoute, CheckVehicle, ThirdPartyPayment, ThirdPartyPolicy, ThirdPartyZinaraQoute, ZinaraQuote
from config.models import InsuranceApiUrlConfig

# Third Party Only Quote
from config.models import InsuranceApiUrlConfig

# from apirequests.apiurls import ThirdPartyQoute, CheckVehicle, ThirdPartyPayment, ThirdPartyPolicy, RadioQuote,ZinaraQuote, LicensingPayment, LicensingPolicy
# from config.Endpoints import ThirdPartyQoute, ThirdPartyUpdate, ThirdPartyPolicy, LicensingQoute, LicensingPolicy, \
#     LicensingUpdate, CombinedPolicy, CombinedUpdate, CombinedQoute, ComprehensivePolicy, REVERSAL


#
# @permission_classes((AllowAny,))
# class TokenView(views.APIView):
#     def get(self, request):
#         response = requests.get(url=Yako + '/v2/icecash-token/')
#         if response.status_code == 200:
#             data = response.json()
#             token = data['token']
#             res = {"message": "%s" % token}
#             return Response(res, status=status.HTTP_200_OK)

class PolicyReversalView(views.APIView):

    def get(self, request):

        if request.method == 'GET':
            original_partner_ref = request.GET.get('original_partner_reference')
            try:
                quote = requests.get(
                    REVERSAL()[0]['api_endpoint'] + '?original_partner_reference=' + original_partner_ref )
                res = quote.json()
                print(res, 'Json request')
                return Response(res, status=status.HTTP_200_OK)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Outrisk For Service"}
                return HttpResponse(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class ComprehensiveView(views.APIView):
    """
    Key for request_type (INT):
        1 =  Quote
        2 =  Update
        3 =  Retrieve Policy
    """

    def get(self, request):

        if request.method == 'GET':
            vrn = request.GET.get('vrn')
            durationMonths = request.GET.get('duration_months')
            vehicle_type = request.query_params.get('vrn_type', None)
            vrn_usage = request.query_params.get('vrn_usage', None)
            suminsured = request.query_params.get('suminsured', None)
            product = request.query_params.get('product', None)

            vrn_type_icecash = request.query_params.get('vrn_type_icecash', None)
            vrn_usage_icecash = request.query_params.get('vrn_usage_icecash', None)

            try:
                quote = requests.get('http://196.43.100.211:3005/comprehensive/quote/' + '?suminsured=' + suminsured + '&product=' + product +
                    '&vrn=' + vrn + '&vrn_type=' + vehicle_type + '&vrn_usage=' + vrn_usage + '&duration_months=' + durationMonths + '&vrn_usage_icecash=' + vrn_usage_icecash + '&vrn_type_icecash=' + vrn_type_icecash)
                res = quote.json()
                print(res, 'Json request')
                return Response(res, status=status.HTTP_200_OK)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Outrisk For Service"}
                return HttpResponse(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class ThirdPartyView(views.APIView):
    """
    Key for request_type (INT):
        1 =  Quote
        2 =  Update
        3 =  Retrieve Policy
    """

    def get(self, request):
        print('ive arrived')
        request_type = request.GET.get('request_type')

        if request.method == 'GET' and request_type == '1':
            vrn = request.GET.get('vrn')
            durationMonths = request.GET.get('duration_months')
            vehicle_type = request.query_params.get('vrn_type', None)
            tax_class = request.query_params.get('tax_class', None)
            print(request_type, vrn, tax_class, durationMonths, vehicle_type, ThirdPartyQoute())
            print(ThirdPartyQoute() + '?vrn=' + vrn + '&duration_months=' + durationMonths +
                  '&vrn_type=' + vehicle_type + '&tax_class=' + tax_class)
            try:
                # quote = requests.get(
                #     ThirdPartyQoute() + '?vrn=' + vrn + '&duration_months=' + durationMonths +
                #     '&vrn_type=' + vehicle_type + '&tax_class=' + tax_class)

                quote = requests.get(ThirdPartyQoute() + '?vrn=' + vrn + '&duration_months=' + durationMonths + '&tax_class='+tax_class + '&vrn_type='+vehicle_type)
                res = quote.json()
                print(res, 'Json request')
                return Response(res, status=status.HTTP_200_OK)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Outrisk For Service"}
                return HttpResponse(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        elif request.method == 'GET' and request_type == '2':
            paymentMethod = request.GET.get('payment_method')
            IDnumber = request.GET.get('client_idnumber')
            insuranceID = request.GET.get('insurance_id')
            payment_status = request.GET.get('payment_status')
            msisdn = request.GET.get('client_mobile')
            print(paymentMethod, IDnumber, insuranceID, payment_status, msisdn)
            try:
                payment_update = requests.get(ThirdPartyPayment() + '?payment_method=' + paymentMethod + '&client_idnumber=' + IDnumber + '&insurance_id=' + insuranceID +
                                              '&payment_status=' + payment_status + '&client_mobile=' + msisdn)
                res = payment_update.json()
                print(res, 'Json request')
                return HttpResponse(res, status=status.HTTP_200_OK)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Outrisk For Service"}
                return HttpResponse(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        elif request.method == 'GET' and request_type == '3':
            insuranceID = request.GET.get('insuranceID')

            try:
                retrieve_policy = requests.get(ThirdPartyPolicy() + '?insuranceID=' + insuranceID)
                res = retrieve_policy.json()
                print(res, 'Json request')
                return Response(res, status=status.HTTP_200_OK)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Outrisk For Service"}
                return Response(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class LicensingView(views.APIView):
    """
    Key for request_type (INT):
        1 =  Quote
        2 =  Update
        3 =  Retrieve Policy
    """

    def get(self, request):
        request_type = request.GET.get('request_type')

        if request.method == 'GET' and request_type == '1':
            print('im here')
            vrn = request.GET.get('vrn')
            IDnumber = request.GET.get('client_id_number')
            radio_usage = request.GET.get('radio_usage')
            LicFrequency = request.GET.get('frequency')
            radio_type = "0"
            if(request.GET.get('radio_type') is not None ):
                radio_type = request.GET.get('radio_type')

            product_type = request.GET.get('type')
            vehicle_type = request.query_params.get('vrn_type', None)
            tax_class = request.query_params.get('tax_class', None)
            print('-------------------------------- DEBUG ---------------------------------')
            print(f"vrn: { vrn }, Lic Frequency: { LicFrequency }, ID_number: { IDnumber }, radio: { radio_type }, radio type: {radio_type}")
            print('-------------------------------- DEBUG ---------------------------------')
            try:
                # quote = requests.get(
                #     ThirdPartyZinaraQoute() + '?vrn=' + vrn + '&type=' + product_type + '&client_id_number='
                #     + IDnumber + '&radio_usage=' + radio_usage + '&frequency=' + LicFrequency
                #     + '&vrn_type=' + vehicle_type + '&tax_class=' + tax_class)
                
                quote = requests.get(ZinaraQuote() + '?vrn=' + vrn + '&frequency=' + LicFrequency + '&client_id_number='
                                     + IDnumber + "&radio_usage="+radio_usage + "&radio_type="+radio_type)
                res = quote.json()
                print(res, 'Json request')
                return Response(res, status=status.HTTP_200_OK)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Outrisk For Service"}
                return Response(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        elif request.method == 'GET' and request_type == '2':
            paymentMethod = request.GET.get('payment_method')
            IDnumber = request.GET.get('client_idnumber')
            licenceID = request.GET.get('licence_id')
            payment_status = request.GET.get('payment_status')
            msisdn = request.GET.get('client_mobile')
            deliveryMethod = request.GET.get('delivery_method')
            try:
                payment_update = requests.get(
                    LicensingUpdate()[0]['api_endpoint'] + '?payment_method=' + paymentMethod +
                    '&client_idnumber=' + IDnumber + '&licence_id=' + licenceID +
                    '&payment_status' + payment_status + '&client_mobile='
                    + msisdn + '&delivery_method=' + deliveryMethod)
                res = payment_update.json()
                print(res, 'Json request')
                return Response(res, status=status.HTTP_200_OK)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Outrisk For Service"}
                return Response(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        elif request.method == 'GET' and request_type == '3':
            licenceID = request.GET.get('licence_id')

            try:
                retrieve_policy = requests.get(LicensingPolicy()[0]['api_endpoint'] + '?licence_id=' + licenceID)
                res = retrieve_policy.json()
                print(res, 'Json request')
                return Response(res, status=status.HTTP_200_OK)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Outrisk For Service"}
                return HttpResponse(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class CombinedView(views.APIView):
    """
    Key for request_type (INT):
        1 =  Quote
        2 =  Update
        3 =  Retrieve Policy
    """

    def get(self, request):
        request_type = request.GET.get('request_type')
        if request.method == 'GET' and request_type == '1':

            vrn = request.GET.get('vrn')
            idnumber = request.GET.get('id_number')
            LicFrequency = request.GET.get('frequency')
            durationMonths = request.GET.get('duration_months')
            radio_usage = request.query_params.get('radio_usage')
            vehicle_type = request.query_params.get('vrn_type', None)
            tax_class = request.query_params.get('tax_class', None)
            try:
                quote = requests.get(
                    CombinedQoute()[0]['api_endpoint'] + '?vrn=' + vrn + '&duration_months='
                    + durationMonths + '&id_number='
                    + idnumber + '&frequency=' + LicFrequency + '&radio_usage=' + radio_usage +
                    '&vrn_type=' + vehicle_type + '&tax_class=' + tax_class)
                res = quote.json()
                print(res, 'Json request')
                return Response(res, status=status.HTTP_200_OK)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Outrisk For Service"}
                return Response(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        elif request.method == 'GET' and request_type == '2':

            paymentMethod = request.GET.get('payment_method')
            combinedid = request.GET.get('combined_id')
            payment_status = request.GET.get('payment_status')
            msisdn = request.GET.get('client_mobile')
            deliveryMethod = request.GET.get('delivery_method')
            try:
                payment_update = requests.get(CombinedUpdate()[0]['api_endpoint'] + '?payment_method=' + paymentMethod +
                                              '&combined_id=' + combinedid +
                                              '&payment_status' + payment_status + '&client_mobile='
                                              + msisdn + '&delivery_method=' + deliveryMethod)
                res = payment_update.json()
                print(res, 'Json request')
                return Response(res, status=status.HTTP_200_OK)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Outrisk For Service"}
                return Response(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        elif request.method == 'GET' and request_type == '3':
            combinedID = request.GET.get('combined_id')

            try:
                retrieve_policy = requests.get(CombinedPolicy()[0]['api_endpoint'] + '?combined_id=' + combinedID)
                res = retrieve_policy.json()
                print(res, 'Json request')
                return Response(res, status=status.HTTP_200_OK)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Outrisk For Service"}
                return Response(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)
