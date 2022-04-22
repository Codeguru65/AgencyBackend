from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import requests
import json
from django.shortcuts import render
from commission.serializer import SalesSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from authentication.models import User
from commission.models import AgentSale

# Third Party Only Quote
from config.Endpoints import ThirdPartyQoute, ThirdPartyUpdate, ThirdPartyPolicy, LicensingQoute, LicensingPolicy, \
    LicensingUpdate, CombinedPolicy, CombinedUpdate, CombinedQoute, ComprehensivePolicy, REVERSAL


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
                quote = requests.get(
                    ComprehensivePolicy()[0]['api_endpoint'] + '?suminsured=' + suminsured + '&product=' + product +
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
            print(request_type, vrn, tax_class, durationMonths, vehicle_type, ThirdPartyQoute()[0]['api_endpoint'])
            print(ThirdPartyQoute()[0]['api_endpoint'] + '?vrn=' + vrn + '&duration_months=' + durationMonths +
                  '&vrn_type=' + vehicle_type + '&tax_class=' + tax_class)
            try:
                quote = requests.get(
                    ThirdPartyQoute()[0]['api_endpoint'] + '?vrn=' + vrn + '&duration_months=' + durationMonths +
                    '&vrn_type=' + vehicle_type + '&tax_class=' + tax_class)
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
                payment_update = requests.get(ThirdPartyUpdate()[0][
                                                  'api_endpoint'] + '?payment_method=' + paymentMethod + '&client_idnumber=' + IDnumber + '&insurance_id=' + insuranceID +
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
                retrieve_policy = requests.get(ThirdPartyPolicy()[0]['api_endpoint'] + '?insuranceID=' + insuranceID)
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
            product_type = request.GET.get('type')
            vehicle_type = request.query_params.get('vrn_type', None)
            tax_class = request.query_params.get('tax_class', None)
            print(vrn, product_type, IDnumber, radio_usage, LicFrequency, vehicle_type, tax_class)
            try:
                quote = requests.get(
                    LicensingQoute()[0]['api_endpoint'] + '?vrn=' + vrn + '&type=' + product_type + '&client_id_number='
                    + IDnumber + '&radio_usage=' + radio_usage + '&frequency=' + LicFrequency
                    + '&vrn_type=' + vehicle_type + '&tax_class=' + tax_class)
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
                retrieve_policy = requests.get(LicensingPolicy()[0]['api_endpoint'] + '?licence_id=' + licenceID + "&request_type=3")
                print(f'i am here ---> {retrieve_policy} ')
                res = retrieve_policy.json()
                # print(res, 'Json request')
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


class AgentSaleView(views.APIView):
    
    def post(self, request):
        # serializer = SalesSerializer(data=request.data)

        data_unicord = request.body.decode('utf-8')
        data  = json.loads(data_unicord)

        print(f'data {data}')
        owner = User.objects.get(id=request.user.id)
        price_category = owner.institution.agent_category.price

        commissionable = data['commissionable']
        commission = float(commissionable) * price_category

        

        try:
            AgentSale.objects.create(
                agent=request.user,
                agent_category=owner.institution.agent_category.category,
                agent_institution=owner.institution.name,
                agent_pricing=owner.institution.agent_category.price,
                product_name=data['product_name'],
                vrn=data['vrn'],
                transaction_id= data['transaction_id'],
                policy_number = data['policy_number'],
                receipt_number=data['receipt_number'],
                transaction_amount=data['transaction_amount'],
                transaction_commission=round(commission, 2),
                transaction_status=data['transaction_status'],
                commission_month=datetime.now().strftime("%m-%Y"),
                customer_name = data['customer_name'],
                customer_email = data['customer_email'],
                customer_cell = data['customer_cell'],
                customer_IDnumber = data['customer_IDnumber']
                )

            return Response(data, status=status.HTTP_201_CREATED)

        except:
                return Response(detail='there was an error saving the sale', status=status.HTTP_400_BAD_REQUEST)

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
