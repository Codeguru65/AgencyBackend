from django.urls import path

from .InsuranceZinara import ThirdPartyZinaraView, ThirdPartyZinaraPaymentView, ThirdPartyZinaraPolicyView
from .licensing import RadioQouteView, ZinaraQouteView, LicensingPaymentView, LicensingPolicyView
from .views import ThirdPartyQouteView, ThirdPartyPaymentView, ThirdPartyPolicyView

urlpatterns = [
    path('rta_quote/', ThirdPartyQouteView.as_view(), name="rta_quote"),
    path('rta_update/', ThirdPartyPaymentView.as_view(), name="rta_update"),
    path('rta_policy/', ThirdPartyPolicyView.as_view(), name="rta_policy"),

    path('radio_quote/', RadioQouteView.as_view(), name="radio_quote"),
    path('zinara_quote/', ZinaraQouteView.as_view(), name="zinara_quote"),
    path('licensing_update/', LicensingPaymentView.as_view(), name="licensing_update"),
    path('licensing_policy/', LicensingPolicyView.as_view(), name="licensing_policy"),

    path('combo_quote/', ThirdPartyZinaraView.as_view(), name="combo_quote"),
    path('combo_update/', ThirdPartyZinaraPaymentView.as_view(), name="combo_update"),
    path('combo_policy/', ThirdPartyZinaraPolicyView.as_view(), name="combo_policy"),

]
