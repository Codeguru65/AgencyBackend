import requests
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from commission.models import AgentSale
from django.contrib.auth.models import User
from datetime import datetime


from apirequests.apiurls import RadioQuote, \
    ZinaraQuote, LicensingPayment, LicensingPolicy
from config.models import InsuranceApiUrlConfig


# Radio Quote
class RadioQouteView(views.APIView):
    vrn_param_config = openapi.Parameter('vrn', in_=openapi.IN_QUERY, description='vehicle registration number',
                                         type=openapi.TYPE_STRING)
    duration_param_config = openapi.Parameter('LicFrequency', in_=openapi.IN_QUERY,
                                              description='vehicle registration number',
                                              type=openapi.TYPE_STRING)
    clientID_param_config = openapi.Parameter('IDnumber', in_=openapi.IN_QUERY,
                                              description='vehicle registration number',
                                              type=openapi.TYPE_STRING)
    type_param_config = openapi.Parameter('type', in_=openapi.IN_QUERY,
                                          description='vehicle registration number',
                                          type=openapi.TYPE_STRING)
    usage_param_config = openapi.Parameter('radio_usage', in_=openapi.IN_QUERY,
                                           description='vehicle registration number',
                                           type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[vrn_param_config, duration_param_config, clientID_param_config,
                                            type_param_config, usage_param_config])
    def get(self, request):
        vrn = request.GET.get('vrn')
        LicFrequency = request.GET.get('LicFrequency')
        client_id_number = request.GET.get('client_id_number')
        vrn_type = request.GET.get('vrn_type')
        radio_usage = request.GET.get('radio_usage')
        cover_period = request.GET.get('cover_period')
        tax_class = request.GET.get('tax_class')

        if request.method == 'GET':
            
            print("============================================== DEBUG ============================================")
            print(f"vrn: { vrn }, LicFrequency: { LicFrequency }, id Number: { client_id_number }, type: {vrn_type}, radio usage: {radio_usage}, tax class: { tax_class }")
            print("============================================== DEBUG ============================================")
            try:
                quote = requests.get(RadioQuote() + '?vrn=' + vrn + '&frequency=' + LicFrequency + '&client_id_number='
                                     + client_id_number + '&type=' + vrn_type + '&radio_usage=' + radio_usage + "&tax_class="+tax_class)
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


# Zinara Quote
class ZinaraQouteView(views.APIView):
    vrn_param_config = openapi.Parameter('vrn', in_=openapi.IN_QUERY, description='vehicle registration number',
                                         type=openapi.TYPE_STRING)
    duration_param_config = openapi.Parameter('LicFrequency', in_=openapi.IN_QUERY,
                                              description='vehicle registration number',
                                              type=openapi.TYPE_STRING)
    clientID_param_config = openapi.Parameter('IDnumber', in_=openapi.IN_QUERY,
                                              description='vehicle registration number',
                                              type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[vrn_param_config, duration_param_config, clientID_param_config])
    def get(self, request):
        vrn = request.GET.get('vrn')
        LicFrequency = request.GET.get('LicFrequency')
        ID_number = request.GET.get('client_id_number')
        vrn_type = request.GET.get("vrn_type")
        radio_usage = request.GET.get("radio_usage")

        
        print("================================================= DEBUG ======================================================")
        print(f"vrn: { vrn }, Lic Frequency: { LicFrequency }, ID_number: { ID_number }, radio: { radio_usage }")
        print("================================================= DEBUG ======================================================")

        if request.method == 'GET':
            try:
                quote = requests.get(ZinaraQuote() + '?vrn=' + vrn + '&frequency=' + LicFrequency + '&client_id_number='
                                     + ID_number + "&radio_usage="+radio_usage)
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

class LicensingPaymentView(views.APIView):
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
    licenceID_param_config = openapi.Parameter('licenceID', in_=openapi.IN_QUERY,
                                               description='Insurance ID',
                                               type=openapi.TYPE_STRING)
    tran_status_param_config = openapi.Parameter('status', in_=openapi.IN_QUERY,
                                                 description='Transaction Status',
                                                 type=openapi.TYPE_STRING)
    deliveryMethod_param_config = openapi.Parameter('deliveryMethod', in_=openapi.IN_QUERY,
                                                    description='Transaction Status',
                                                    type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[paymentMethod_param_config, msisdn_param_config,
                                            IDnumber_param_config, licenceID_param_config, tran_status_param_config,
                                            deliveryMethod_param_config])
    def get(self, request):
        paymentMethod = request.GET.get('paymentMethod')
        IDnumber = request.GET.get('IDnumber')
        licenceID = request.GET.get('licenceID')
        tran_status = request.GET.get('status')
        client_mobile = request.GET.get('client_mobile')
        delivery_method = request.GET.get('deliveryMethod')

        print("=========================================================== DEBUG =======================================================")
        print(f"py method: {paymentMethod}, id: {IDnumber}, licID: {licenceID}, trans_stat: {tran_status}, client_mobile: {client_mobile}, del_method: {delivery_method}")
        print("=========================================================== DEBUG =======================================================")
        if request.method == 'GET':
            try:
                tran_update = requests.get(LicensingPayment() + '?payment_method=' + paymentMethod +
                                           '&client_idnumber=' + IDnumber + '&licence_id=' + licenceID +
                                           '&payment_status=' + tran_status + "&client_mobile=" + client_mobile  + "&request_type=2" + "&delivery_method=" + delivery_method)
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
class LicensingPolicyView(views.APIView):
    licenceID_param_config = openapi.Parameter('licenceID', in_=openapi.IN_QUERY,
                                         type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[licenceID_param_config])
    def get(self, request):
        licenceID = request.GET.get('licenceID')
        insuranceID = request.GET.get('insuranceID')
        
        # product_name = "Radio License" if request.GET.get("type") == "Radio" else "Zinara Insurance"

        print("==================================================== DEBUG ===================================================")
        print(f"licence id: {licenceID}, insuranceID {insuranceID}")
        print("==================================================== DEBUG ===================================================")

        if request.method == 'GET':
            try:

                quote = requests.get(LicensingPolicy() + '?licence_id=' + licenceID + "&request_type=3")
                res = quote.json()

                print("==================================================== DEBUG ===================================================")
                print(f"response json { res }")
                print("==================================================== DEBUG ===================================================")
                if res['Response']['Status'] == "Approved":
                    print('Qoutes Succesful ................... creating transaction')
                    
                    owner = request.user
                    
                    # owner = User.objects.get(id=request.user.id)
                    price_category = owner.institution.agent_category.price
                    #commission = float(res['Response']['TotalAmount']) * price_category

                    # for zinara only        


                    

                    AgentSale.objects.create(
                        agent=request.user,
                        agent_category=owner.institution.agent_category.category,
                        agent_institution=owner.institution.name,
                        agent_pricing=owner.institution.agent_category.price,
                        product_name= "Radio Licence" if request.GET.get("type") == "Radio" else "Zinara Insurance",
                        vrn=res['Response']['VRN'],
                        transaction_id=licenceID,        
                        policy_number = "n/a",                
                        # policy_number=res['Response']['PolicyNo'],
                        receipt_number = res['Response']['ReceiptID'],
                        transaction_amount=float(res['Response']['TotalAmount']),
                        transaction_commission=0.0,
                        transaction_status=res['Response']['Status'],
                        commission_month=datetime.now().strftime("%m-%Y")
                        # transaction_date = models.DateTimeField(auto_now=True),
                    )

                    # Mark: create Agent sale object for radio only

                    
                    return Response(res, status=status.HTTP_200_OK)
                else:
                    message = {"message": res}
                    return Response(message, status=status.HTTP_202_ACCEPTED)

            except ConnectionError as e:
                res = {"message": "Service Unavailable, Contact Xarani For Service"}
                return Response(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)