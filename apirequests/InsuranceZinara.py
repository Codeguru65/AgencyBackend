from datetime import datetime

import requests
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from datetime import datetime

from apirequests.apiurls import RadioQuote, \
    ZinaraQuote, LicensingPayment, LicensingPolicy, ThirdPartyZinaraQoute, ThirdPartyZinaraPayment, \
    ThirdPartyZinaraPolicy
from authentication.models import User
from commission.models import AgentSale
from config.models import InsuranceApiUrlConfig



class ThirdPartyZinaraView(views.APIView):
    vrn_param_config = openapi.Parameter('vrn', in_=openapi.IN_QUERY, description='vehicle registration number',
                                         type=openapi.TYPE_STRING)
    duration_param_config = openapi.Parameter('durationMonths', in_=openapi.IN_QUERY,
                                              description='vehicle registration number',
                                              type=openapi.TYPE_STRING)
    clientID_param_config = openapi.Parameter('idnumber', in_=openapi.IN_QUERY,
                                              description='vehicle registration number',
                                              type=openapi.TYPE_STRING)
    LicFrequency_param_config = openapi.Parameter('LicFrequency', in_=openapi.IN_QUERY,
                                                  description='vehicle registration number',
                                                  type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[vrn_param_config, duration_param_config,
                                            clientID_param_config, LicFrequency_param_config])
    def get(self, request):
        vrn = request.GET.get('vrn')
        LicFrequency = request.GET.get('LicFrequency')
        id_number = request.GET.get('id_number')
        durationMonths = request.GET.get('duration_months')
        vrn_type = request.GET.get("vrn_type")
        radio_usage = "Radio"
        tax_class = request.GET.get("tax_class")
        print(f" vrn: {vrn}, LicFrequency: {LicFrequency}, ID Number: {id_number}, Duration Months: { durationMonths} vrn_type: { vrn_type }, tax_class: { tax_class }")

        if request.method == 'GET':
            try:
                quote = requests.get(
                    ThirdPartyZinaraQoute() + 
                    '?vrn=' + vrn + 
                    "&id_number="+id_number + 
                    "&frequency="+LicFrequency + 
                    "&radio_usage="+radio_usage +
                    "&vrn_type="+vrn_type +
                    "&tax_class="+tax_class +
                    "&duration_months="+durationMonths,
                )
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


# Licensing Payment

class ThirdPartyZinaraPaymentView(views.APIView):
    paymentMethod_param_config = openapi.Parameter('paymentMethod', in_=openapi.IN_QUERY, description='Payment Method '
                                                                                                      '-> Refer to '
                                                                                                      'documentation',
                                                   type=openapi.TYPE_STRING)
    msisdn_param_config = openapi.Parameter('msisdn', in_=openapi.IN_QUERY,
                                            description='Mobile number',
                                            type=openapi.TYPE_STRING)
    combinedid_param_config = openapi.Parameter('combinedid', in_=openapi.IN_QUERY,
                                                description='Insurance ID',
                                                type=openapi.TYPE_STRING)
    tran_status_param_config = openapi.Parameter('status', in_=openapi.IN_QUERY,
                                                 description='Transaction Status',
                                                 type=openapi.TYPE_STRING)
    deliveryMethod_param_config = openapi.Parameter('deliveryMethod', in_=openapi.IN_QUERY,
                                                    description='Transaction Status',
                                                    type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[paymentMethod_param_config, msisdn_param_config,
                                            combinedid_param_config, tran_status_param_config,
                                            deliveryMethod_param_config])
    def get(self, request):
        paymentMethod = request.GET.get('paymentMethod')
        combinedid = request.GET.get('combinedid')
        deliveryMethod = request.GET.get('deliveryMethod')
        tran_status = request.GET.get('status')
        client_mobile = request.GET.get('client_mobile')
        id_number = request.GET.get("IDnumber")
        if request.method == 'GET':
            
            print("========================================================== DEBUG ===================================================")
            print(f"payment: {paymentMethod}, combined id: {combinedid}, payment status: {tran_status}, client mobile: {client_mobile}, delivery method: {deliveryMethod}")
            print("========================================================== DEBUG ===================================================")
            
            try:
                tran_update = requests.get(ThirdPartyZinaraPayment() + '?payment_method=' + paymentMethod +
                                           '&combined_id=' + combinedid + '&delivery_method=' + deliveryMethod +
                                           '&payment_status=' + tran_status + '&client_mobile=' + client_mobile + 
                                           "&request_type=2" + "&id_number="+id_number) 
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
class ThirdPartyZinaraPolicyView(views.APIView):
    combinedID_param_config = openapi.Parameter('combinedID', in_=openapi.IN_QUERY,
                                                type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[combinedID_param_config])
    def get(self, request):
        combinedID = request.GET.get('combinedID')
        if request.method == 'GET':

            print("================================================== DEBUG =========================================================")
            print(f"combined ID: {combinedID}")
            print("================================================== DEBUG =========================================================")
            try:
                quote = requests.get(ThirdPartyZinaraPolicy() + '?combined_id=' + combinedID + "&request_type=3")
                res = quote.json()
                print("================================================== DEBUG =========================================================")
                print(f"result: {res}")
                print("================================================== DEBUG =========================================================")
                if res['Response']['Status'] == 'Approved':
                    print('Qoutes Succesful lets create save the transaction now')
                    # Process Commission Sharing
                    owner = User.objects.get(id=request.user.id)
                    price_category = owner.institution.agent_category.price
                    commission = float(res['Response']['PremiumAmount']) * price_category

                    AgentSale.objects.create(
                        agent=request.user,
                        agent_category=owner.institution.agent_category.category,
                        agent_institution=owner.institution.name,
                        agent_pricing=owner.institution.agent_category.price,
                        product_name='Third Party Insurance (RTA) -Less Zinara',
                        vrn=res['Response']['VRN'],
                        transaction_id=combinedID,
                        policy_number=res['Response']['CombinedID'],
                        receipt_number=res['Response']['ReceiptID'],
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
