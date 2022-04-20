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
from commission.models import AgentSale
from config.models import AgencyPricing
from apirequests.apiurls import ThirdPartyQoute, CheckVehicle, ThirdPartyPayment, ThirdPartyPolicy
from config.models import InsuranceApiUrlConfig


# Third Party Processing
class ThirdPartyQouteView(views.APIView):
    vrn_param_config = openapi.Parameter('vrn', in_=openapi.IN_QUERY, description='vehicle registration number',
                                         type=openapi.TYPE_STRING)
    duration_param_config = openapi.Parameter('durationMonths', in_=openapi.IN_QUERY,
                                              description='vehicle registration number',
                                              type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[vrn_param_config, duration_param_config])
    def get(self, request):
        vrn = request.GET.get('vrn')
        durationMonths = request.GET.get('durationMonths')
        tax_class = request.GET.get('tax_class')
        vehicle_type = request.GET.get('vehicle_type')

        print(f"tax class --> {tax_class}, ")
        print(f"vrn: { vrn }, derationMonths: { durationMonths }, tax_class: { tax_class }, vehicle_type: { vehicle_type}")
        if request.method == 'GET':
            try:
                quote = requests.get(ThirdPartyQoute() + '?vrn=' + vrn + '&duration_months=' + durationMonths + '&tax_class='+tax_class + '&vrn_type='+vehicle_type)
                res = quote.json()
                print(res, 'Json request')
                if res['Response']['Result'] == 1:
                    print('Qoutes Succesful lets create save the transaction now')
                    owner = request.user.id
                    print(owner)

                    return Response(res, status=status.HTTP_200_OK)
                else:
                    message = {"message": res}
                    return Response(message, status=status.HTTP_202_ACCEPTED)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Xarani For Service"}
                return Response(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# Third Party Payment
class ThirdPartyPaymentView(views.APIView):
    paymentMethod_param_config = openapi.Parameter('paymentMethod', in_=openapi.IN_QUERY, description='Payment Method '
                                                                                                      '-> Refer to '
                                                                                                      'documentation',
                                                   type=openapi.TYPE_STRING)
    msisdn_param_config = openapi.Parameter('msisdn', in_=openapi.IN_QUERY,
                                            description='Mobile number',
                                            type=openapi.TYPE_STRING)
    IDnumber_param_config = openapi.Parameter('IDnumber', in_=openapi.IN_QUERY,
                                              description='Client Identity number',
                                              type=openapi.TYPE_STRING)
    insuranceID_param_config = openapi.Parameter('insuranceID', in_=openapi.IN_QUERY,
                                                 description='Insurance ID',
                                                 type=openapi.TYPE_STRING)
    tran_status_param_config = openapi.Parameter('status', in_=openapi.IN_QUERY,
                                                 description='Transaction Status',
                                                 type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[paymentMethod_param_config, msisdn_param_config,
                                            IDnumber_param_config, insuranceID_param_config, tran_status_param_config])
    def get(self, request):
        paymentMethod = request.GET.get('paymentMethod')
        IDnumber = request.GET.get('client_idnumber')
        insuranceID = request.GET.get('insurance_id')
        tran_status = request.GET.get('payment_status')
        msisdn = request.GET.get('msisdn')
        client_mobile = request.GET.get('client_mobile')
        
        print("================================================= DEBUG ====================================================")
        print(f"pament method: {paymentMethod}, ID number: {IDnumber}, insuaranceID: {insuranceID}, client_mobile: {client_mobile}, status: { tran_status }")
        print("================================================= DEBUG ====================================================")
        if request.method == 'GET':
            try:
                tran_update = requests.get(ThirdPartyPayment() + '?payment_method=' + paymentMethod +
                                           '&client_idnumber=' + IDnumber + '&insurance_id=' + insuranceID +
                                           '&payment_status=' + tran_status + "&client_mobile=" + client_mobile  + "&request_type=2")
                res = tran_update.json()
                print(res, 'Json request')
                if res['Response']['Result'] == 1:
                    print('Qoutes Succesful lets create save the transaction now')
                    owner = request.user.id
                    print(owner)

                    return Response(res, status=status.HTTP_200_OK)
                else:
                    message = {"message": res}
                    return Response(message, status=status.HTTP_202_ACCEPTED)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Xarani For Service"}
                return Response(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# Third Party Policy
class ThirdPartyPolicyView(views.APIView):
    insuranceID_param_config = openapi.Parameter('insuranceID', in_=openapi.IN_QUERY,
                                                 type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[insuranceID_param_config])
    def get(self, request):
        insuranceID = request.GET.get('insuranceID')
        if request.method == 'GET':
            try:
                quote = requests.get(ThirdPartyPolicy() + '?insuranceID=' + insuranceID)
                res = quote.json()
                print(res, 'Json request')
                if res['Response']['Status'] == 'Approved':
                    print('Qoutes Succesful lets create save the transaction now')
                    # Process Commission Sharing
                    owner = User.objects.get(id=request.user.id)
                    price_category = owner.institution.agent_category.price
                    commission = float(res['Response']['Amount']) * price_category

                    print("================================================= DEBUG ====================================================")
                    print(f"owner: {owner}, price_category: {price_category}, commision {commission}")
                    print("================================================= DEBUG ====================================================")

                    

                    AgentSale.objects.create(
                        agent=request.user,
                        agent_category=owner.institution.agent_category.category,
                        agent_institution=owner.institution.name,
                        agent_pricing=owner.institution.agent_category.price,
                        product_name='Third Party Insurance (RTA)',
                        vrn=res['Response']['VRN'],
                        transaction_id=insuranceID,
                        policy_number=res['Response']['PolicyNo'],
                        # receipt_number = res['Response']['ReceiptID'],
                        transaction_amount=float(res['Response']['Amount']),
                        transaction_commission=round(commission, 2),
                        transaction_status=res['Response']['Status'],
                        commission_month=datetime.now().strftime("%m-%Y")
                        # transaction_date = models.DateTimeField(auto_now=True),
                    )
                    return Response(res, status=status.HTTP_200_OK)
                else:
                    message = {"message": res}
                    return Response(message, status=status.HTTP_202_ACCEPTED)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Xarani For Service"}
                return Response(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)
